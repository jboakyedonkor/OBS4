from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
from testPostgres import updateMethods, checkMethods, insertMethods
import requests
import os
import sys
import jwt

goog_api = Blueprint('goog_api', __name__)


def get_quote():
    api_url = "https://sandbox.tradier.com/v1/markets/quotes"
    api_key = "Jo5Qmiac0PqN8dG360REQq8oGbNY"
    response = requests.get(api_url, params={'symbols': 'GOOGL'}, headers={'Accept':
                                                                               'application/json',
                                                                           'Authorization': 'Bearer ' + api_key})

    response = response.json()
    response = response['quotes']['quote']
    return response


@goog_api.route('/gen_token/<username>', methods=['GET'])
def generate_token(username):
    current_time = datetime.utcnow()
    exp_time = current_time + \
               timedelta(seconds=0, minutes=30, hours=0)
    payload = {'username': username,
               'iss': 'goog_API',
               'exp': exp_time
               }
    SECRET_KEY = os.getenv('SECRET_KEY')
    token = jwt.encode(payload, key=str(SECRET_KEY), algorithm='HS256')
    return jsonify({'token': token.decode('UTF-8')})


@goog_api.route('/goog/share_price', methods=['GET'])
def get_price():
    return jsonify({"Price": get_quote()['last']})


def token_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'goog_key' in request.headers:
            token = request.headers['goog_key']
        if not token:
            return Flask.make_response(jsonify({'error': 'Missing token'}), 401)
        try:
            SECRET_KEY = os.getenv('SECRET_KEY')
            data = jwt.decode(token, str(SECRET_KEY))
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)
        except jwt.InvalidSignatureError:
            return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)
        except jwt.InvalidTokenError:
            return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)
        return f(current_user, *args, **kwargs)
    return decorated


@goog_api.route('/goog/buy/')
@token_check
def buy_shares(current_user):
    if checkMethods.checkUsername(current_user) == True:
        symbol = 'GOOG'
        amount = request.args.get('amount')
        updateMethods.update_bank_table(symbol, amount, True)
        updateMethods.update_stock_table(symbol, amount, True)
        insertMethods.insert_transaction_logs_table(symbol, get_quote()['last'], amount, current_user, 'Buy')
        return jsonify('Bought')
    else:
        return jsonify('Error - user not found')


@goog_api.route('/goog/sell/')
@token_check
def sell_shares(current_user):
    if checkMethods.checkUsername(current_user) == True:
        symbol = 'GOOG'
        amount = request.args.get('amount')
        updateMethods.update_bank_table(symbol, amount, False)
        updateMethods.update_stock_table(symbol, amount, False)
        insertMethods.insert_transaction_logs_table(symbol, get_quote()['last'], amount, current_user, 'Sell')
        return jsonify('Sold')
    else:
        return jsonify('Error - user not found')

@goog_api.route('/goog/shares/')
@token_check
def total_shares(current_user):
    if checkMethods.checkUsername(current_user) == True:
        googNetWorth = get_quote()['last']*checkMethods.getUserNetworth(current_user)
        return jsonify(googNetWorth)
    else:
        return jsonify('Error - user not found')

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(goog_api)
    app.run()
