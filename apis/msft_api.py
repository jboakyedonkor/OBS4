import requests
import os
import sys
import jwt
import dotenv
from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
from app.apis.models.msft_models import db, Stock, Transaction

# from flask_sqlalchemy import SQLAlchemy

# TODO Change path to ../config/.env when not debugging
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))


microsoft_api = Blueprint('microsoft_api', __name__)


def get_token(headers):
    """
    Get auth token from request headers
    """
    if 'Authorization' not in headers or not headers['Authorization']:
        return None

    token = headers['Authorization']
    return token


def generate_token(username, key, seconds=0, minutes=30, hours=0):
    """
    Generates JWT tokens
    """
    current_time = datetime.utcnow()
    exp_time = current_time + \
        timedelta(seconds=seconds, minutes=minutes, hours=hours)

    payload = {'username': username,
               'iss': 'Microsoft_API',
               'exp': exp_time
               }

    token = jwt.encode(payload, key=key, algorithm='HS256')
    return token


def verify_token(token, key):
    """
    Verify that JWT token is valid
    """
    try:
        payload = jwt.decode(token, key, algorithms='HS256')

        # check if the issuer of the token it this API
        if payload['iss'] == 'Microsoft_API':
            return True, payload['username']
        else:
            return False, 'invalid iss'

    except jwt.ExpiredSignatureError:
        return False, 'token expired'

    except jwt.InvalidSignatureError:
        return False, 'invalid signature'

    except jwt.InvalidTokenError:
        return False, 'invalid token'


def get_quote():
    """
    Get market quotes for Micrsoft using the Tradier API
    """
    api_url = "https://sandbox.tradier.com/v1/markets/quotes"
    api_key = os.getenv("API_KEY")

    params = {'symbols': 'MSFT'}

    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer ' + api_key
               }

    response = requests.get(api_url, params=params, headers=headers)
    response = response.json()
    response = response['quotes']['quote']
    return response


@microsoft_api.route('/msft/gen_token', methods=['POST'])
def gen_token():
    """
    Route for gnera
    """
    db.create_all()
    user_info = request.get_json()
    if not user_info:

        return Flask.make_response(
            jsonify({'error': 'wrong  format'}), 400)

    user = user_info['user']

    secret_key = os.getenv('SECRET_KEY')
    token = generate_token(user, secret_key)
    token.decode()

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
        return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    # check if the auth token was valid
    if not valid:
        return Flask.make_response(jsonify({'error': msg}), 400)

    buy_response = None
    user = msg
    api_response = get_quote()

    # update the stock price in the database
    msft_stock = Stock.query.filter_by(
        symbol=api_response['symbol']).first()

    if not msft_stock:
        msft_stock = Stock(
            symbol=api_response['symbol'],
            price=api_response['last'])
        db.session.add(msft_stock)

    else:
        msft_stock.price = api_response['last']

    # process purchase request
    purchase_request = request.get_json()

    # check purchase request has valid json
    if purchase_request and 'shares' in purchase_request.keys():

        # update stock information
        payment = api_response['last'] * purchase_request['shares']
        # msft_stock.shares -= purchase_request['shares']

        # to Transaction entry
        transaction = Transaction(
            user=user,
            symbol=api_response['symbol'],
            payment=payment,
            share_price=api_response['last'],
            shares_bought=purchase_request['shares'],
            shares_sold=None)

        transaction_response = {
            'user': user,
            'symbol': transaction.symbol,
            'share_price': transaction.share_price,
            'shares_bought': transaction.shares_bought,
            'created_at': transaction.created_at,
            'payment': transaction.payment
        }

        # add transcation to session
        db.session.add(transaction)
        buy_response = jsonify(transaction_response)

    # incorrect request json
    else:
        db.session.commit()
        return Flask.make_response(
            jsonify({'error': 'improper json'}), 400)

    db.session.commit()

    return buy_response


@microsoft_api.route('/msft/sell', methods=['POST'])
def sell_share():
    """
    Route for selling a share of Microsoft stock
    """

    token = get_token(request.headers)
    if not token:
        return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    # check if the auth token was valid
    if not valid:
        return Flask.make_response(jsonify({'error': msg}), 400)

    sell_response = None
    user = msg

    api_response = get_quote()
    # update the stock price in the database
    msft_stock = Stock.query.filter_by(
        symbol=api_response['symbol']).first()

    if not msft_stock:
        msft_stock = Stock(
            symbol=api_response['symbol'],
            price=api_response['last'])
        db.session.add(msft_stock)

    else:
        msft_stock.price = api_response['last']

    # process purchase request
    purchase_request = request.get_json()

    # check purchase request has valid json
    if purchase_request and 'shares' in purchase_request.keys():

        # update stock information
        payment = api_response['last'] * purchase_request['shares']
        msft_stock.shares -= purchase_request['shares']

        # to Transaction entry
        transaction = Transaction(
            user=user,
            symbol=api_response['symbol'],
            payment=payment,
            share_price=api_response['last'],
            shares_bought=None,
            shares_sold=purchase_request['shares'])

        transaction_response = {
            'user': user,
            'symbol': transaction.symbol,
            'share_price': transaction.share_price,
            'shares_sold': transaction.shares_sold,
            'created_at': transaction.created_at,
            'payment': transaction.payment
        }

        # add transcation to session
        db.session.add(transaction)
        sell_response = Flask.make_response(jsonify(transaction_response), 200)

    # incorrect request json
    else:
        db.session.commit()
        return Flask.make_response(
            jsonify({'error': 'improper json'}), 400)

    db.session.commit()

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
        return Flask.make_response(jsonify({'error': msg}), 400)

    # TODO implement logging
    user = msg
    api_response = get_quote()
    response = {
        'symbol': api_response['symbol'],
        'name': api_response['description'],
        'share_price': api_response['last'],
    }

    # update the stock price in the database
    msft_stock = Stock.query.filter_by(
        symbol=api_response['symbol']).first()

    if not msft_stock:
        msft_stock = Stock(
            symbol=api_response['symbol'],
            price=api_response['last'])
        db.session.add(msft_stock)

    msft_stock.price = api_response['last']
    db.session.commit()

    return jsonify(response)


"""
@microsoft_api.route('/msft/shares', methods=['GET'])
def get_shares():

    #Route for get the amount of share

    token = get_token(request.headers)
    if not token:
        return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    if not valid:
        return Flask.make_response(jsonify({'error': msg}), 400)

    # TODO implement logging
    user = msg

    api_response = get_quote()

    # query database for msft_stock
    msft_stock = Stock.query.filter_by(
        symbol=api_response['symbol']).first()

    if not msft_stock:
        msft_stock = Stock(
            symbol=api_response['symbol'],
            price=api_response['last'])
        db.session.add(msft_stock)
    else:
        msft_stock.price = api_response['last']
    db.session.commit()

    response = {
        'symbol': api_response['symbol'],
        'name': api_response['description'],
        'shares': msft_stock.shares,
    }

    return jsonify(response)
"""

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
    db.init_app(app)
    app.register_blueprint(microsoft_api)
    app.run()
