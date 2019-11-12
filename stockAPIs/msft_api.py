import requests
import os
import sys
import jwt
import dotenv
from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
sys.path.append(os.getcwd())
from db.models import Stock

# from flask_sqlalchemy import SQLAlchemy

# TODO Change path to ../config/.env when not debugging
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))


microsoft_api = Blueprint('microsoft_api', __name__)


def get_token(headers):
    if 'Authorization' not in headers or not headers['Authorization']:
        return None

    token = headers['Authorization']
    return token


def generate_token(username, key, seconds=0, minutes=30, hours=0):
    """
    generates JWT token
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
    verify that JWT token is valid
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


def get_quote():
    """
    get market quotes for Micrsoft using the Tradier API
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
    user_info = request.get_json()
    if not user_info:

        return Flask.make_response(
            jsonify({'error': 'wrong  format'}), 400)

    username = user_info['username']

    secret_key = os.getenv('SECRET_KEY')
    token = generate_token(username, secret_key)
    token.decode()

    return jsonify({'token': token.decode()})


@microsoft_api.route('/msft/buy', methods=['POST'])
def buy_share():
    """
    Route for buying a share of Microsoft stock
    """
    # if request.method == 'POST':

    return '/msft/buy'


@microsoft_api.route('/msft/sell', methods=['POST'])
def sell_share():
    """
    Route for selling a share of Microsoft stock
    """
    return '/msft/sell'


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
    else:
        # TODO implement logging
        username = msg
        api_response = get_quote()
        response = {
            'symbol': api_response['symbol'],
            'name': api_response['description'],
            'share_price': api_response['last'],
        }
    return jsonify(response)


@microsoft_api.route('/msft/shares', methods=['GET'])
def get_shares():
    """
    Route for get the amount of share
    """
    token = get_token(request.headers)
    if not token:
        return Flask.make_response(jsonify({'error': 'Invalid token'}), 400)

    secret_key = os.getenv('SECRET_KEY')
    valid, msg = verify_token(token.encode(), secret_key)

    if not valid:
        return Flask.make_response(jsonify({'error': msg}), 400)
    else:
        #       TODO implement logging
        username = msg
        api_response = get_quote()
        response = {
            'symbol': api_response['symbol'],
            'name': api_response['description'],
            'shares': 5000,
        }

    return jsonify(response)


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(microsoft_api)
    app.run()
