import pyrebase
import dotenv
import os
import jwt
from datetime import datetime, timedelta
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))


def intialize_firebase():
    config = {
        "apiKey": os.getenv("AAPL_FIRE_API_KEY"),
        "authDomain": os.getenv("AAPL_AUTH_DOMAIN"),
        "databaseURL": os.getenv("AAPL_DATABASE_URL"),
        "projectId": os.getenv("AAPL_PROJECT_ID"),
        "storageBucket": os.getenv("AAPL_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("AAPL_MESS_SENDER_ID"),
        "appId": os.getenv("AAPL_APP_ID")
    }

    firebase = pyrebase.initialize_app(config)
    return firebase

# Generates token


def generate_token(username, seconds=0, minutes=30, hours=0):

    exp_time = datetime.utcnow() + \
        timedelta(seconds=seconds, minutes=minutes, hours=hours)

    payload = {'username': username,
               'exp': exp_time
               }

    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token
