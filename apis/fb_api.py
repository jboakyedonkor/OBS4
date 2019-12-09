"""
Modules include sql ORM, time formatting, http requests, and secret key storage.
"""
import pyrebase
import dotenv
from datetime import datetime, timedelta
import os
import sys
import jwt
from flask import Flask, request, jsonify
import requests
sys.path.append(os.getcwd())
dotenv.load_dotenv(dotenv_path='.\\config\\.env')

app = Flask(__name__)

config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DB_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MSG_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
}

fire_db = pyrebase.initialize_app(config).database()


@app.route('/api/user/verify', methods=['GET', 'POST'])
def verify_user():
    token = request.headers.get('token')

    if token is None:
        return jsonify(
            status=400,
            description='Authentication token not sent.',
            authenticated=False)

    decoded = jwt.decode(token, os.getenv('SECRET_KEY'), algorithm='HS256')

    return jsonify(
        status=200,
        description='User is authenticated.',
        authenticated=True,
        user=decoded['username'])


@app.route('/fb/share_price', methods=['GET'])
def get_price():
    response = requests.get(
        'https://sandbox.tradier.com/v1/markets/quotes',
        params={
            'symbols': 'FB',
            'greeks': 'false'},
        headers={
            'Authorization': 'Bearer ' + os.getenv('FB_ACCESS_TOKEN'),
            'Accept': 'application/json'})
    fb_quote = response.json()['quotes']['quote']
    return jsonify(
        symbol=fb_quote['symbol'],
        name=fb_quote['description'],
        share_price=fb_quote['last'])


@app.route('/api/transactions/FB', methods=['POST'])
def create_transaction():
    new_transaction = {
        "created_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "payment": request.json['payment'],
        "share_price": request.json['price'],
        "symbol": "FB",
        "username": request.json['username']
    }

    if (request.json['trans_type'] == 'BUY'):
        new_transaction['shares_bought'] = request.json['amount']
        fire_db.child('transactions').child(request.json['username']).child('bought').push(new_transaction)
    elif (request.json['trans_type'] == 'SELL'):
        new_transaction['shares_sold'] = request.json['amount']
        fire_db.child('transactions').child(request.json['username']).child('sold').push(new_transaction)

    return jsonify(new_transaction)


@app.route('/api/transactions/admin/FB', methods=['GET', 'POST'])
def get_FB_transactions():
    all_transactions = fire_db.child('transactions').get()
    return jsonify(all_transactions.val())


@app.route('/fb/buy', methods=['POST'])
def buy_share():
    verify = requests.get('http://localhost:5002/api/user/verify',
                          headers={'token': request.headers.get('token')})

    try:
        verify.json()
    except BaseException:
        return jsonify(error='Invalid token.')

    symbol = "FB"
    num_owned = request.json["amount"]
    username = verify['user']
    price = requests.get(
        'http://localhost:5002/fb/share_price').json()['share_price']
    trans_type = "BUY"
    pl = 0
    pl_added = num_owned * price

    try:
        user_asset = fire_db.child('assets').order_by_child(
            'username').equal_to(username).get().val()
        user_asset_info = list(user_asset.items())[0][1]
        user_asset_key = list(user_asset.items())[0][0]
    except BaseException:
        user_asset = None

    try:
        bank_asset = fire_db.child('assets').order_by_child(
            'username').equal_to('obs@04.ssgj').get().val()
    except BaseException:
        bank_asset = None

    if bank_asset is None:
        bank_pl = 5000 * price * -1
        new_bank = {
            "symbol": "FB",
            "pl": bank_pl,
            "num_owned": 5000,
            "username": "obs@04.ssgj"}
        fire_db.child('assets').push(new_bank)
        requests.post(
            'http://localhost:5000/api/transactions/FB',
            json={
                'payment': -1 * 5000 * price,
                'trans_type': 'BUY',
                'amount': 5000,
                'username': "obs@04.ssgj",
                'price': price})
        bank_asset = fire_db.child('assets').order_by_child(
            'username').equal_to('obs@04.ssgj').get().val()

    bank_asset_key = list(bank_asset.items())[0][0]
    bank_asset_info = list(bank_asset.items())[0][1]

    if bank_asset_info['num_owned'] < num_owned:
        asset_diff = num_owned - bank_asset_info['num_owned']
        bank_asset_info['num_owned'] += asset_diff + 5000
        bank_asset_info['pl'] += (asset_diff + 5000) * price * -1
        fire_db.child('assets').child(bank_asset_key).update(bank_asset_info)
        requests.post(
            'http://localhost:5000/api/transactions/FB',
            json={
                'payment': -1 * price * (asset_diff + 5000),
                'trans_type': 'BUY',
                'amount': asset_diff + 5000,
                'username': "obs@04.ssgj",
                'price': price})

    bank_asset_info["num_owned"] -= num_owned
    bank_asset_info["pl"] += num_owned * price
    fire_db.child('assets').child(bank_asset_key).update(bank_asset_info)

    if user_asset is not None:
        user_asset_info["num_owned"] += num_owned
        user_asset_info["pl"] -= num_owned * price
        fire_db.child('assets').child(user_asset_key).update(user_asset_info)
        requests.post(
            'http://localhost:5000/api/transactions/FB',
            json={
                'payment': -1 * price * num_owned, 
                'trans_type': 'BUY',
                'amount': num_owned,
                'username': username,
                'price': price})
        return jsonify(
            user=username,
            symbol='FB',
            share_price=price,
            shares_bought=num_owned,
            created_at=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            payment=pl_added)
    else:
        new_asset = {
            "symbol": symbol,
            "pl": num_owned * price * -1,
            "num_owned": num_owned,
            "username": username}
        fire_db.child('assets').push(new_asset)
        requests.post(
            'http://localhost:5000/api/transactions/FB',
            json={
                'payment': -1 * price * num_owned,
                'trans_type': 'BUY',
                'amount': num_owned,
                'username': username,
                'price': price})
        return jsonify(
            user=username,
            symbol='FB',
            share_price=price,
            shares_bought=num_owned,
            created_at=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            payment=pl_added)


@app.route('/fb/sell', methods=['POST'])
def sell_share():
    verify = requests.get('http://localhost:5000/api/user/verify',
                          headers={'token': request.headers.get('token')})

    try:
        verify.json()
    except BaseException:
        return jsonify(error='Invalid token.')

    symbol = "FB"
    num_owned = request.json["amount"]
    username = verify['user']
    price = requests.get(
        'http://localhost:5000/fb/share_price').json()['share_price']
    trans_type = "SELL"
    pl = 0
    pl_added = num_owned * price

    try:
        user_asset = fire_db.child('assets').order_by_child(
            'username').equal_to(username).get().val()
        user_asset_info = list(user_asset.items())[0][1]
        user_asset_key = list(user_asset.items())[0][0]
    except BaseException:
        user_asset = None

    try:
        bank_asset = fire_db.child('assets').order_by_child(
            'username').equal_to('obs@04.ssgj').get().val()
    except BaseException:
        bank_asset = None

    if bank_asset is None:
        bank_pl = 5000 * price * -1
        new_bank = {
            "symbol": "FB",
            "pl": bank_pl,
            "num_owned": 5000,
            "username": "obs@04.ssgj"}
        fire_db.child('assets').push(new_bank)
        requests.post(
            'http://localhost:5000/api/transactions/FB',
            json={
                'payment': price * 5000,
                'trans_type': 'BUY',
                'amount': 5000,
                'username': "obs@04.ssgj",
                'price': price})
        bank_asset = fire_db.child('assets').order_by_child(
            'username').equal_to('obs@04.ssgj').get().val()

    bank_asset_key = list(bank_asset.items())[0][0]
    bank_asset_info = list(bank_asset.items())[0][1]

    bank_asset_info["num_owned"] += num_owned
    bank_asset_info["pl"] -= num_owned * price
    fire_db.child('assets').child(bank_asset_key).update(bank_asset_info)

    if user_asset is not None:
        if user_asset_info["num_owned"] < num_owned:
            return jsonify(
                status=400,
                error='User does not have enough assets to sell.')
        user_asset_info["num_owned"] -= num_owned
        user_asset_info["pl"] += num_owned * price
        fire_db.child('assets').child(user_asset_key).update(user_asset_info)
        requests.post(
            'http://localhost:5000/api/transactions/FB',
            json={
                'payment': num_owned * price,
                'trans_type': 'SELL',
                'amount': num_owned,
                'username': username,
                'price': price})
        return jsonify(
            user=username,
            symbol='FB',
            share_price=price,
            shares_sold=num_owned,
            created_at=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            payment=pl_added)
    else:
        return jsonify(error='User does not exist.')


if __name__ == "__main__":
    # app.run('0.0.0.0', 5000, debug=True)
    app.run(port=5002)
