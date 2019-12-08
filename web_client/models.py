from datetime import datetime
from web_client import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    account1 = db.Column(db.JSON)
    account2 = db.Column(db.JSON)
    account3 = db.Column(db.JSON)

    def __repr__(self):
        return f"Users('{self.username}', '{self.email}')"

