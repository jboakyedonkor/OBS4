from datetime import datetime
from web_client import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    account_name = db.Column(db.String(20), unique=True, nullable=False)
    cash = db.Column(db.Decimal, nullable=False)
    msft_shares = db.Column(db.Integer, nullable=False)
    fb_shares = db.Column(db.Integer, nullable=False)
    goog_shares = db.Column(db.Integer, nullable=False)
    aapl_shares = db.Column(db.Integer, nullable=False)
