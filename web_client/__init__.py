from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_login import LoginManager
import os
import dotenv
import psycopg2
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("USER_POSTGRES")

import os
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