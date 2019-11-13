import requests
from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
import json
import datetime
import pyrebase
from app import firebase,app,db,dbfire
from functools import wraps

aapl_api = Blueprint('aapl_api', __name__)

    # Generates Token
@aapl_api.route('/gen/<username>')
def generate_token( seconds=0, minutes=30, hours=0):
  
    exp_time =  datetime.datetime.utcnow() + \
        timedelta(seconds=seconds, minutes=minutes, hours=hours)

    payload = {'username': request.args.get('username'),
               'iss': 'appl_api',
               'exp': exp_time,
               'troll': 'troll_by_santiago'
               }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token':token.decode('UTF-8')})

# Makes decorater to confirm token was put in for api use
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
       
        if 'aapl_token' in request.headers:
            token = request.headers['aapl_token']
        if not token:
            return jsonify({'message': 'Token Missing'}),401
        try:
            data = jwt.decode(token, os.environ.get("SECRET_KEY"))
            # current_user = Share.query.filter_by(username = data['username'])  
            current_user = data['username']
        # except:
        #     return jsonify({'message': 'Token is invalid'}),401
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        return f(current_user,*args,**kwargs)
    return decorated

@aapl_api.route('/aapl/share_price')
def get_price():
    price = aapl_price()
    return jsonify({"Price" : price['quotes']['quote']['last']})

@aapl_api.route('/aapl/buy/')
@token_required
def buy_shares(current_user):
    amount = request.args.get('amount')
    price = aapl_price()['quotes']['quote']['last']
    buy = round(float(amount) * price,2)
    data = {
    'symbol': 'AAPL',
    "Bought": buy,
    "Amount": amount,
    "Purchase Price": price,
    "time":  str(datetime.datetime.now())
    }
    dbfire.child("Bought").child(current_user).push(data)
    # print(current_user)
    return 'Bought'

@aapl_api.route('/aapl/sell/')
@token_required
def sell_shares(current_user):
    amount = request.args.get('amount')
    price = aapl_price()['quotes']['quote']['last']
    sell = round(float(amount) * price,2)
    data = {
    'symbol': 'AAPL',
    "Sold": sell,
    "Amount": amount,
    "Purchase Price": price,
    "time":  str(datetime.datetime.now())
    }
    dbfire.child("Sell").child(current_user).push(data)
    return 'Sold'

@aapl_api.route('/aapl/shares/')
@token_required
def total_shares(current_user):
    # shares = Share.query.filter_by(id=id).all();
    # output = []
    # for share in shares:
    #     if(share['id'] == id):
    #         share_data={}
    #         share_data['user'] = share.id
    #         share_data['symbol'] = share.symbol
    #         share_data['price'] = share.price
    #         share_data['shares'] = share.shares
    #         output.append(share_data)
    # return jsonify({'shares':output})
    all_users = dbfire.child("Bought").child(current_user).get()
    output = []
    #Checks if any purchases in database
    if(all_users.each() is None):
            return jsonify({"Total Shares":" No apple stock purchased"})
    for user in all_users.each():
        
        
        #print(user.val()) # {name": "Mortimer 'Morty' Smith"}
        output.append(user.val())
    # print(all_users)
    return jsonify({"Total Shares":output})

def aapl_price():
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes', 
                    params={'symbols': 'AAPL'}, 
                    headers={'Accept': 'application/json','Authorization': 'Bearer q7HoHM5iKOZ1WGou3gguoTqle4VF'})
    json_response = response.json()
    return json_response

if __name__ == "__main__":
    app.register_blueprint(aapl_api)
    