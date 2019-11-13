# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# import pyrebase
# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__)
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'


# """Base config, uses staging database server."""
# # DEBUG = False
# # TESTING = False
# # DB_SERVER = '192.168.1.56'
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'app.db') or \
# 'sqlite:///' + os.path.join(basedir, 'app.db')
# SECRET_KEY = os.environ.get("SECRET_KEY")
# if not SECRET_KEY:
#     raise ValueError("No SECRET_KEY set for Flask application")
# app.config['SECRET_KEY'] = SECRET_KEY

# config={
#     "apiKey": "AIzaSyBdMIAVR_ozMR0PB09nsqG0b9yUDRhwq_k",
#     "authDomain": "learn-6087d.firebaseapp.com",
#     "databaseURL": "https://learn-6087d.firebaseio.com",
#     "projectId": "learn-6087d",
#     "storageBucket": "learn-6087d.appspot.com",
#     "messagingSenderId": "866078852777",
#     "appId": "1:866078852777:web:0773bcd7852e7858ebcbb8"
# }

# firebase = pyrebase.initialize_app(config)
# dbfire = firebase.database()
# from app import routes