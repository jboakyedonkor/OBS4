import pyrebase
import dotenv
import jwt
import os
import requests
from datetime import datetime, timedelta


def create_firebase_app():

    env_file = ".{}config{}.env".format(os.sep, os.sep)
    dotenv.load_dotenv(dotenv_path=env_file)
    config = {

        "apiKey": os.getenv('MSFT_FIREBASE_API_KEY'),
        "authDomain": os.getenv('MSFT_FIREBASE_AUTH_DOMAIN'),
        "databaseURL": os.getenv('MSFT_FIREBASE_DB_URL'),
        "projectId": os.getenv('MSFT_FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('MSFT_FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('MSFT_FIREBASE_MSG_SENDER_ID'),
        "appId": os.getenv('MSFT_FIREBASE_APP_ID')

    }
   # print(config)
    if config["apiKey"]:
        firebase = pyrebase.initialize_app(config)
        return firebase
    else:
        return None


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
    #print(os.getenv("MSFT_TRADIER_API_KEY")

    api_url = "https://sandbox.tradier.com/v1/markets/quotes"
    api_key = os.getenv("MSFT_TRADIER_API_KEY")

    params = {'symbols': 'MSFT'}

    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer ' + api_key
               }

    response = requests.get(api_url, params=params, headers=headers)
    response = response.json()
    response = response['quotes']['quote']
    return response
