"""Modules include sql ORM, time formatting, http requests, and secret key storage."""
from datetime import datetime, timedelta
import os
import sys
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
from models.Users import User, UserSchema
from models.FBTransactions import FBTransaction, FBTransactionSchema
from models.Assets import Asset, AssetSchema
import dotenv
sys.path.append(os.getcwd())

dotenv.load_dotenv(dotenv_path='./config/.env')

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db_temp.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)
transaction_FB_schema = FBTransactionSchema()
transactions_FB_schema = FBTransactionSchema(many=True)

@app.route('/api/user/register', methods=['POST'])
def register_user():
    if (db.session.query(User.user_id).filter_by(email=request.json['email']).scalar() is not None):
        return jsonify(status=400, description='User already exists.')

    email = request.json['email']
    password = request.json['password']

    secret = os.getenv('SERVER_KEY')
    payload = {'email': email, 'password': password, 'login_time': str(datetime.now()), 'token_expire': str(datetime.now() + timedelta(hours=1))}
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

    new_user = User(email, password, encoded_jwt)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/api/user/login', methods=['POST'])
def login_user():
    if (db.session.query(User.user_id).filter_by(email=request.json['email']).scalar() is None):
        return jsonify(status=400, description='User does not exist.')

    user_cred_check = User.query.filter_by(email=request.json['email']).first()

    if user_cred_check.password == request.json['password']:
        secret = os.getenv('SERVER_KEY')
        payload = {'email': user_cred_check.email, 'password': user_cred_check.password, 'login_time': str(datetime.now()), 'token_expire': str(datetime.now() + timedelta(hours=1))}
        encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

        user_cred_check.token = encoded_jwt

        db.session.commit()

        return user_schema.jsonify(user_cred_check)
    else:
        return jsonify(status=400, description='Incorrect password.')

@app.route('/api/user/logout', methods=['POST'])
def logout_user():
    if (db.session.query(User.user_id).filter_by(email=request.json['email']).scalar() is None):
        return jsonify(status=400, description='User does not exist.')

    user_logout = User.query.filter_by(email=request.json['email']).first()

    user_logout.token = None

    db.session.commit()

    return user_schema.jsonify(user_logout)

@app.route('/api/user/verify', methods=['GET'])
def verify_user():
    token = request.headers.get('token')
    
    if token is None:
        return jsonify(status=400, description='Authentication token not sent.', authenticated=False)

    decoded = jwt.decode(token, os.getenv('SERVER_KEY'), algorithm='HS256')

    if datetime.strptime(decoded['token_expire'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():
        return jsonify(status=400, description='Authentication token has expired.', authenticated=False)

    return jsonify(status=200, description='User is authenticated.', authenticated=True)

@app.route('/api/quotes/FB', methods=['GET'])
def get_price():
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                            params={'symbols': 'FB', 'greeks': 'false'},
                            headers={'Authorization': os.getenv('FB_ACCESS_TOKEN'),
                                     'Accept': 'application/json'})
    fb_quote = response.json()['quotes']['quote']
    return jsonify(symbol=fb_quote['symbol'], description=fb_quote['description'], quote=fb_quote['last'])

@app.route('/api/transactions/FB', methods=['POST'])
def create_transaction():
    timestamp = datetime.now()
    trans_type = request.json['trans_type']
    amount = request.json['amount']
    price = request.json['price']
    user_id = request.json['user_id']

    new_transaction = FBTransaction(timestamp, amount, trans_type, price, user_id)

    db.session.add(new_transaction)
    db.session.commit()

    return transaction_FB_schema.jsonify(new_transaction)

@app.route('/api/transactions/admin/FB', methods=['GET', 'POST'])
def get_FB_transactions():
    all_transactions = FBTransaction.query.all()
    result = transactions_FB_schema.dump(all_transactions)
    return jsonify(result)

@app.route('/api/assets/FB', methods=['POST'])
def fb_assets():
    verify = requests.get('http://localhost:5000/api/user/verify', 
                          headers={'token': request.headers.get('token')}).json()

    if verify['authenticated'] == False:
        return jsonify(status=400, description='User not authenticated.')

    symbol = 'FB'
    num_owned = request.json['amount']
    user_id = request.json['user_id']
    price = requests.get('http://localhost:5000/api/quotes/FB').json()['quote']
    trans_type = request.json['type']
    pl = 0
    pl_added = num_owned * price
    user_asset = Asset.query.filter_by(user_id=request.json['user_id'], symbol=symbol).first()

    bank_asset = Asset.query.filter_by(user_id=0, symbol=symbol).first()
    if bank_asset is None:
        bank_pl = 5000 * price * -1
        new_bank = Asset('FB', bank_pl, 5000, 0)
        db.session.add(new_bank)
        db.session.commit()
        requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': num_owned, 'user_id': 0, 'price': price})
        bank_asset = Asset.query.filter_by(user_id=0, symbol=symbol).first()

    if trans_type == 'BUY':
        if bank_asset.num_owned < num_owned:
            asset_diff = num_owned - bank_asset.num_owned
            bank_asset.num_owned += asset_diff + 5000
            bank_asset.pl += (asset_diff + 5000) * price * -1
            db.session.commit()
            requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': asset_diff + 5000, 'user_id': 0, 'price': price})

        bank_asset.num_owned -= num_owned
        bank_asset.pl += num_owned * price

        if user_asset is not None:
            user_asset.num_owned += num_owned
            user_asset.pl -= num_owned * price
            db.session.commit()
            requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': num_owned, 'user_id': user_id, 'price': price})
        else:
            new_user = Asset(symbol, num_owned*price*-1, num_owned, request.json['user_id'])
            db.session.add(new_user)
            db.session.commit()
            requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'BUY', 'amount': num_owned, 'user_id': user_id, 'price': price})
    else:
        bank_asset.num_owned += num_owned
        bank_asset.pl -= num_owned * price

        if user_asset is not None:
            if user_asset.num_owned < num_owned:
                return jsonify(status = 400, description = 'User does not have enough assets to sell.')
            user_asset.num_owned -= num_owned
            user_asset.pl += num_owned * price
            db.session.commit()
            requests.post('http://localhost:5000/api/transactions/FB', json={'trans_type': 'SELL', 'amount': num_owned, 'user_id': user_id, 'price': price})
        else:
            return jsonify(status=400, description='User does not have any assets to sell.')


if __name__ == "__main__":
    app.run('localhost', 5000, debug=True)