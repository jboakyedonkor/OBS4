import os
import sys
import jwt
import dotenv
from datetime import datetime, timedelta
from flask import Flask, Blueprint, jsonify, request
from msft_helpers import *

# from flask_sqlalchemy import SQLAlchemy

# TODO Change path to ../config/.env when not debugging

env_file = ".{}config{}.env".format(os.sep, os.sep)
dotenv.load_dotenv(dotenv_path=env_file)

microsoft_api = Blueprint('microsoft_api', __name__)

fire_db = create_firebase_app().database()


@microsoft_api.route('/msft/gen_token', methods=['POST'])
def gen_token():
    """
    Route for gnera
    """
    user_info = request.get_json()
    if not user_info:

        return jsonify({'error': 'wrong  format'})

    user = user_info['user']

    secret_key = os.getenv('SECRET_KEY')
    token = generate_token(user, secret_key)

    return jsonify({'token': token.decode()})


@microsoft_api.route('/msft/buy', methods=['POST'])
def buy_share():
    """
    Route for buying a share of Microsoft stock

    the request json should look like
    {
        shares: amt_of_shares
    }

    """
    # get token from headers
    token = get_token(request.headers)
    if not token:
        return jsonify({'error': 'Invalid token'})

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    # check if the auth token was valid
    if not valid:
        return jsonify({'error': msg})

    buy_response = None
    user = msg
    api_response = get_quote()

    # process purchase request
    purchase_request = request.get_json()

    # check purchase request has valid json
    if purchase_request and 'shares' in purchase_request.keys():

        # update stock information
        payment = api_response['last'] * purchase_request['shares']
        # msft_stock.shares -= purchase_request['shares']

        transaction_response = {
            'user': user,
            'symbol': api_response['symbol'],
            'share_price': api_response['last'],
            'shares_bought': purchase_request['shares'],
            'created_at': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            'payment': payment
        }

        # store into firebase
        fire_db.child('transactions').push(transaction_response)

        buy_response = jsonify(transaction_response)

    # incorrect request json
    else:
        return jsonify({'error': 'improper json request'})

    return buy_response


@microsoft_api.route('/msft/sell', methods=['POST'])
def sell_share():
    """
    Route for selling a share of Microsoft stock
    """
    token = get_token(request.headers)
    if not token:
        return jsonify({'error': 'Invalid token'})

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    # check if the auth token was valid
    if not valid:
        return jsonify({'error': msg})

    sell_response = None
    user = msg
    api_response = get_quote()

    # process purchase request
    purchase_request = request.get_json()

    # check purchase request has valid json
    if purchase_request and 'shares' in purchase_request.keys():

        # update stock information
        payment = api_response['last'] * purchase_request['shares']
        # msft_stock.shares -= purchase_request['shares']

        transaction_response = {
            'user': user,
            'symbol': api_response['symbol'],
            'share_price': api_response['last'],
            'shares_sold': purchase_request['shares'],
            'created_at': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            'payment': payment
        }

        # store into firebase
        fire_db.child('transactions').push(transaction_response)

        sell_response = jsonify(transaction_response)

    # incorrect request json
    else:
        return jsonify({'error': 'improper json request'})

    return sell_response


@microsoft_api.route('/msft/share_price', methods=['GET'])
def get_price():
    """
    Route for get the price per share of Microsoft  stock
    """
    token = get_token(request.headers)
    if not token:
        return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    if not valid:
        return jsonify({'error': msg})

    user = msg
    api_response = get_quote()

    response = {
        'symbol': api_response['symbol'],
        'name': api_response['description'],
        'share_price': api_response['last'],
    }

    return jsonify(response)


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(microsoft_api)
    app.run()
