from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
import requests
import os
import sys
import jwt
from models.goog_table import updateMethods, insertMethods, checkMethods, clientMethods

app = Flask(__name__)


def get_quote():
    api_url = "https://sandbox.tradier.com/v1/markets/quotes"
    api_key = "Jo5Qmiac0PqN8dG360REQq8oGbNY"
    params = {'symbols': 'GOOGL'}
    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer ' + api_key}
    response = requests.get(
        api_url, params=params, headers=headers)

    response = response.json()
    response = response['quotes']['quote']
    return response


def createNewTable(username):
    clientMethods.create_client_table(username)
    clientMethods.populate_client_table(username)


def generate_token(username):
    current_time = datetime.utcnow()
    exp_time = current_time + \
        timedelta(seconds=0, minutes=30, hours=0)
    payload = {'username': username,
               'exp': exp_time
               }
    SECRET_KEY = os.getenv('welp')
    token = jwt.encode(payload, key=str(SECRET_KEY), algorithm='HS256')
    return token


@app.route('/gen_token/<username>', methods=['GET'])
def showToken(username):
    token = generate_token(username)
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
    if checkMethods.checkTableExists(current_user) is False:
        createNewTable(current_user)

    possibleRemain = checkMethods.checkBankTableStock(symbol) - int(amount)

    if possibleRemain > 0:
        updateMethods.update_bank_table(symbol, amount, True)
        updateMethods.update_client_table(current_user, symbol, amount, True)
        insertMethods.insert_transaction_logs_table(
            symbol, share_price, amount, current_user, 'Buy')
        return jsonify('Bought')

    else:
        updateMethods.update_bank_table(
            symbol, amount - abs(possibleRemain) - 1, True)
        updateMethods.update_client_table(current_user, symbol, amount, True)
        return jsonify('Bought - purchased more than excess')


@app.route('/goog/sell/')
@token_check
def sell_shares(current_user):
    symbol = 'GOOG'
    amount = int(request.headers['amount'])
    share_price = get_quote()['last']

    if checkMethods.checkTableExists(current_user) is False:
        createNewTable(current_user)

    possibleRemain = checkMethods.checkClientTableStock(
        symbol, current_user) - int(amount)
    if possibleRemain > 0:
        updateMethods.update_bank_table(symbol, amount, False)
        updateMethods.update_client_table(current_user, symbol, amount, False)
        insertMethods.insert_transaction_logs_table(
            symbol, share_price, amount, current_user, 'Sell')
        return jsonify('Sold')
    else:
        return jsonify('Error - client lacks stocks to sell')


@app.route('/goog/shares', methods=['GET'])
@token_check
def total_shares(current_user):
    symbol = 'GOOG'
    googNetWorth = get_quote(
    )['last'] * checkMethods.checkClientTableStock(symbol, current_user)
    return jsonify(round(float(googNetWorth), 2))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
