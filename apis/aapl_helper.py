import pyrebase
import dotenv
import os
import jwt
import pyrebase
from datetime import datetime, timedelta
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))


def intialize_firebase():
    config = {
        "apiKey": os.getenv("MSFT_FB_API_KEY"),
        "authDomain": os.getenv("MSFT_FB_AUTH_DOMAIN"),
        "databaseURL": os.getenv("MSFT_FB_DB_URL"),
        "projectId": os.getenv("MSFT_FB_PROJECT_ID"),
        "storageBucket": os.getenv("MSFT_FB_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("MSFT_FB_SENDER_ID"),
        "appId": os.getenv("MSFT_FB_APP_ID")
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