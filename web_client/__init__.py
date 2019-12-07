from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_login import LoginManager
import os
import dotenv
import pyrebase
import psycopg2
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("USER_POSTGRES")
# USER_POSTGRES = "postgres://ieigwssk:outuHJVlCsEGUWhlqQc4NDwm3bwouT8X@salt.db.elephantsql.com:5432/ieigwssk"

import os
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))


def intialize_firebase():
    config = {
        "apiKey": os.getenv("STOCK_FIREBASE_API_KEY"),
        "authDomain": os.getenv("STOCK_FIREBASE_AUTH_DOMAIN"),
        "databaseURL": os.getenv("STOCK_FIREBASE_DB_URL"),
        "projectId": os.getenv("STOCK_FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("STOCK_FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("STOCK_FIREBASE_SENDER_ID"),
        "appId": os.getenv("STOCK_FIREBASE_APP_ID")
    }

    firebase = pyrebase.initialize_app(config)
    return firebase

def intialize_login_firebase():
    config = {
        "apiKey": os.getenv("LOGIN_FIREBASE_API_KEY"),
        "authDomain": os.getenv("LOGIN_FIREBASE_AUTH_DOMAIN"),
        "databaseURL": os.getenv("LOGIN_FIREBASE_DB_URL"),
        "projectId": os.getenv("LOGIN_FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("LOGIN_FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("LOGIN_FIREBASE_SENDER_ID"),
        "appId": os.getenv("LOGIN_FIREBASE_APP_ID")
    }
    
    firebase = pyrebase.initialize_app(config)
    return firebase
    
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User will be logged out after 30 minutes
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

from web_client import routes