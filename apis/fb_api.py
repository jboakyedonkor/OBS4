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

def get_token(headers):
    if 'token' not in headers or not headers['token']:
        return None

    token = headers['token']
    return token


def token_verification(token):
    try:
        decoded = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms='HS256')
        return True, decoded
    except jwt.ExpiredSignatureError:
        return False, None
    except jwt.InvalidSignatureError:
        return False, None


@app.route('/api/user/verify', methods=['GET', 'POST'])
def verify_user():
    token = get_token(request.headers)
    if not token:
        return jsonify(status=400, description='Token not received.', authenticated=False)

    authenticated, decoded = token_verification(token)
    if authenticated:
        return jsonify(
            status=200,
            description='User is authenticated.',
            authenticated=True,
            user=decoded['username'])
    else:
        return jsonify(status=400, description='User not authenticated', authenticated=False, user=None)


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
        Price=fb_quote['last'])


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
    else:
        fire_db.child('transactions').child(request.json['username']).child('test').push(new_transaction)

    return jsonify(new_transaction)


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
    username = verify.json()['user']
    price = requests.get(
        'http://localhost:5000/fb/share_price').json()['Price']
    trans_type = "BUY"
    pl_added = num_owned * price
        
    requests.post(
        'http://localhost:5002/api/transactions/FB',
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
    verify = requests.get('http://localhost:5002/api/user/verify',
                          headers={'token': request.headers.get('token')})

    try:
        verify.json()
    except BaseException:
        return jsonify(error='Invalid token.')

    symbol = "FB"
    num_owned = request.json["amount"]
    username = verify.json()['user']
    price = requests.get(
        'http://localhost:5000/fb/share_price').json()['Price']
    trans_type = "SELL"
    pl_added = num_owned * price

    requests.post(
        'http://localhost:5002/api/transactions/FB',
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


if __name__ == "__main__":
    # app.run('0.0.0.0', 5000, debug=True)
    app.run(port=5002, debug=True)
