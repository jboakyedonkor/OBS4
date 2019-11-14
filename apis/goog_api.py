from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
import requests
import os
import sys
import jwt
from models.goog_models import db, Stock, Transaction
from models.log_db import updateMethods, insertMethods, checkMethods

app = Flask(__name__)

def get_quote():
    api_url = "https://sandbox.tradier.com/v1/markets/quotes"
    api_key = "Jo5Qmiac0PqN8dG360REQq8oGbNY"
    response = requests.get(api_url, params={'symbols': 'GOOGL'}, headers={'Accept':
                                                                               'application/json',
                                                                           'Authorization': 'Bearer ' + api_key})

    response = response.json()
    response = response['quotes']['quote']
    return response


@app.route('/gen_token/<username>', methods=['GET'])
def generate_token(username):
    current_time = datetime.utcnow()
    exp_time = current_time + \
               timedelta(seconds=0, minutes=30, hours=0)
    payload = {'username': username,
               'exp': exp_time
               }
    SECRET_KEY = os.getenv('welp')
    token = jwt.encode(payload, key=str(SECRET_KEY), algorithm='HS256')
    return jsonify({'token': token.decode('UTF-8')})


@app.route('/goog/share_price', methods=['GET'])
def get_price():
    return jsonify({"Price": get_quote()['last']})

def token_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'key' in request.headers:
            token = request.headers['key']
        if not token:
            return jsonify('Error - missing token')
        try:
            SECRET_KEY = os.getenv('welp')
            data = jwt.decode(token, str(SECRET_KEY))
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify('Error - Invalid Token')
        except jwt.InvalidSignatureError:
            return jsonify('Error - Invalid Token')
        except jwt.InvalidTokenError:
            return jsonify('Error - Invalid Token')
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/goog/buy/')
@token_check
def buy_shares(current_user):
    symbol = 'GOOG'
    amount = int(request.headers['amount'])
    share_price = get_quote()['last']
    possibleRemain = checkMethods.checkBankTableStock(symbol) - int(amount)
    if possibleRemain > 0:
        updateMethods.update_bank_table(symbol, amount, True)
        updateMethods.update_client_table(symbol, amount, True)
        insertMethods.insert_transaction_logs_table(symbol, share_price, amount, current_user, 'Buy')
        return jsonify('Bought')
    else:
        updateMethods.update_bank_table(symbol, amount - abs(possibleRemain), True)
        updateMethods.update_client_table(symbol, amount, True)
        return jsonify('Bought - purchased more than excess')


@app.route('/goog/sell/')
@token_check
def sell_shares(current_user):
    symbol = 'GOOG'
    amount = int(request.headers['amount'])
    share_price = get_quote()['last']
    possibleRemain = checkMethods.checkClientTableStock(symbol) - int(amount)
    if possibleRemain > 0:
        updateMethods.update_bank_table(symbol, amount, False)
        updateMethods.update_client_table(symbol, amount, False)
        insertMethods.insert_transaction_logs_table(symbol, share_price, amount, current_user, 'Sell')
        return jsonify('Sold')
    else:
        return jsonify('Error - client lacks stocks to sell')


@app.route('/goog/shares', methods=['GET'])
@token_check
def total_shares(current_user):
    symbol = 'GOOG'
    googNetWorth = get_quote()['last'] * checkMethods.checkClientTableStock('GOOG')
    return jsonify(round(float(googNetWorth), 2))

if __name__ == "__main__":
    app.run()
