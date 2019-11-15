"""Modules include sql ORM, time formatting, http requests, and secret key storage."""
from datetime import datetime, timedelta
import os
import sys
import jwt
from flask import Flask, request, jsonify
import requests
sys.path.append(os.getcwd())
import dotenv
import pyrebase
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
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
}

fire_db = pyrebase.initialize_app(config).database()

@app.route('/api/user/register', methods=['POST'])
def register_user():
    register_user_request = request.get_json()
    
    if not register_user_request:
        return jsonify(status=400, description='You must enter an email and password to register.')

    try:
        user_exist = fire_db.child('users').order_by_child('email').equal_to(register_user_request['username']).get().val()
        return jsonify(error="User already exists.")
    except:
        pass

    email = register_user_request['email']
    password = register_user_request['password']

    secret = os.getenv('SERVER_KEY')
    payload = {'username': email, 'exp': datetime.utcnow() + timedelta(minutes=30)}
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

    new_user = {
        "email": email, 
        "password": password,
        "token": encoded_jwt.decode()
    }
    fire_db.child('users').push(new_user)

    return jsonify(new_user)

@app.route('/api/user/login', methods=['PUT'])
def login_user():
    email = request.json['email']
    password = request.json['password']
    try:
        user_login = fire_db.child('users').order_by_child('email').equal_to(email).get()
        user_key = list(user_login.val().items())[0][0]
        user_info = list(user_login.val().items())[0][1]
    except:
        return jsonify(error='User does not exist.')

    secret = os.getenv('SERVER_KEY')
    payload = {'username': email, 'exp': datetime.utcnow() + timedelta(minutes=30)}
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

    user_info['token'] = encoded_jwt.decode()
    fire_db.child('users').child(user_key).update(user_info)
    return jsonify(user_info)
        

@app.route('/api/user/verify', methods=['GET', 'POST'])
def verify_user():
    token = request.headers.get('token')
    
    if token is None:
        return jsonify(status=400, description='Authentication token not sent.', authenticated=False)

    decoded = jwt.decode(token, os.getenv('SERVER_KEY'), algorithm='HS256')

    return jsonify(status=200, description='User is authenticated.', authenticated=True, user=decoded['username'])

@app.route('/fb/share_price', methods=['GET'])
def get_price():
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                            params={'symbols': 'FB', 'greeks': 'false'},
                            headers={'Authorization': os.getenv('FB_ACCESS_TOKEN'),
                                     'Accept': 'application/json'})
    fb_quote = response.json()['quotes']['quote']
    return jsonify(symbol=fb_quote['symbol'], name=fb_quote['description'], share_price=fb_quote['last'])

@app.route('/api/transactions/FB', methods=['POST'])
def create_transaction():
    new_transaction = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "trans_type": request.json['trans_type'],
        "amount": request.json['amount'],
        "price": request.json['price'],
        "username": request.json['username']
    }

    fire_db.child('transactions').push(new_transaction)

    return jsonify(new_transaction)

@app.route('/api/transactions/admin/FB', methods=['GET', 'POST'])
def get_FB_transactions():
    all_transactions = fire_db.child('transactions').get()
    return jsonify(all_transactions.val())

@app.route('/fb/buy', methods=['POST'])
def buy_share():
    verify = requests.get('http://localhost:5000/api/user/verify', 
                          headers={'token': request.headers.get('token')})

    try:
        verify.json()
    except:
        return jsonify(error='Invalid token.')
    
    symbol = "FB"
    num_owned = request.json["amount"]    
    username = request.json["username"]
    price = requests.get('http://localhost:5000/fb/share_price').json()['share_price']
    trans_type = "BUY"
    pl = 0
    pl_added = num_owned * price

    try:
        user_asset = fire_db.child('assets').order_by_child('username').equal_to(username).get().val()
        user_asset_info = list(user_asset.items())[0][1]
        user_asset_key = list(user_asset.items())[0][0]
    except:
        user_asset = None

    try:
        bank_asset = fire_db.child('assets').order_by_child('username').equal_to('obs@04.ssgj').get().val()
    except:
        bank_asset = None

    if bank_asset is None:
        bank_pl = 5000 * price * -1
        new_bank = { "symbol": "FB", "pl": bank_pl, "num_owned": 5000, "username": "obs@04.ssgj" }
        fire_db.child('assets').push(new_bank)
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': 5000, 'username': "obs@04.ssgj", 'price': price})
        bank_asset = fire_db.child('assets').order_by_child('username').equal_to('obs@04.ssgj').get().val()

    bank_asset_key = list(bank_asset.items())[0][0]
    bank_asset_info = list(bank_asset.items())[0][1]
    
    if bank_asset_info['num_owned'] < num_owned:
        asset_diff = num_owned - bank_asset_info['num_owned']
        bank_asset_info['num_owned'] += asset_diff + 5000
        bank_asset_info['pl'] += (asset_diff + 5000) * price * -1
        fire_db.child('assets').child(bank_asset_key).update(bank_asset_info)
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': asset_diff + 5000, 'username': "obs@04.ssgj", 'price': price})

    bank_asset_info["num_owned"] -= num_owned
    bank_asset_info["pl"] += num_owned * price
    fire_db.child('assets').child(bank_asset_key).update(bank_asset_info)

    if user_asset is not None:
        user_asset_info["num_owned"] += num_owned
        user_asset_info["pl"] -= num_owned * price
        fire_db.child('assets').child(user_asset_key).update(user_asset_info)
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': num_owned, 'username': username, 'price': price})
        return jsonify(user=username, symbol='FB', share_price=price, shares_bought=num_owned, created_at=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'), payment=pl_added)
    else:
        new_asset = { "symbol": symbol, "pl": num_owned*price*-1, "num_owned": num_owned, "username": username }
        fire_db.child('assets').push(new_asset)
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': num_owned, 'username': username, 'price': price})
        return jsonify(user=username, symbol='FB', share_price=price, shares_bought=num_owned, created_at=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'), payment=pl_added)

@app.route('/fb/sell', methods=['POST'])
def sell_share():
    verify = requests.get('http://localhost:5000/api/user/verify', 
                          headers={'token': request.headers.get('token')})

    try:
        verify.json()
    except:
        return jsonify(error='Invalid token.')
    
    symbol = "FB"
    num_owned = request.json["amount"]    
    username = request.json["username"]
    price = requests.get('http://localhost:5000/fb/share_price').json()['share_price']
    trans_type = "SELL"
    pl = 0
    pl_added = num_owned * price

    try:
        user_asset = fire_db.child('assets').order_by_child('username').equal_to(username).get().val()
        user_asset_info = list(user_asset.items())[0][1]
        user_asset_key = list(user_asset.items())[0][0]
    except:
        user_asset = None

    try:
        bank_asset = fire_db.child('assets').order_by_child('username').equal_to('obs@04.ssgj').get().val()
    except:
        bank_asset = None

    if bank_asset is None:
        bank_pl = 5000 * price * -1
        new_bank = { "symbol": "FB", "pl": bank_pl, "num_owned": 5000, "username": "obs@04.ssgj" }
        fire_db.child('assets').push(new_bank)
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': 5000, 'username': "obs@04.ssgj", 'price': price})
        bank_asset = fire_db.child('assets').order_by_child('username').equal_to('obs@04.ssgj').get().val()

    bank_asset_key = list(bank_asset.items())[0][0]
    bank_asset_info = list(bank_asset.items())[0][1]

    bank_asset_info["num_owned"] += num_owned
    bank_asset_info["pl"] -= num_owned * price
    fire_db.child('assets').child(bank_asset_key).update(bank_asset_info)

    if user_asset is not None:
        if user_asset_info["num_owned"] < num_owned:
            return jsonify(status = 400, error = 'User does not have enough assets to sell.')
        user_asset_info["num_owned"] -= num_owned
        user_asset_info["pl"] += num_owned * price
        fire_db.child('assets').child(user_asset_key).update(user_asset_info)
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'SELL', 'amount': num_owned, 'username': username, 'price': price})
        return jsonify(user=username, symbol='FB', share_price=price, shares_sold=num_owned, created_at=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'), payment=pl_added)
    else:
        return jsonify(error='User does not exist.')

if __name__ == "__main__":
    app.run('localhost', 5000, debug=True)