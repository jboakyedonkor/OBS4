from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import pyrebase
app = Flask(__name__)
app.config['SECRET_KEY'] = 'welp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

config={
    "apiKey": "AIzaSyBdMIAVR_ozMR0PB09nsqG0b9yUDRhwq_k",
    "authDomain": "learn-6087d.firebaseapp.com",
    "databaseURL": "https://learn-6087d.firebaseio.com",
    "projectId": "learn-6087d",
    "storageBucket": "learn-6087d.appspot.com",
    "messagingSenderId": "866078852777",
    "appId": "1:866078852777:web:0773bcd7852e7858ebcbb8"
}

firebase = pyrebase.initialize_app(config)
from app import routes