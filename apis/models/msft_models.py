from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Stock (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return ('<Stock {}>'.format(symbol))


class Transaction (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), nullable=False)
    payment = db.Column(db.Float, nullable=False)
    share_price = db.Column(db.Float, nullable=False)
    shares_bought = db.Column(db.Integer)
    shares_sold = db.Column(db.Integer)
    symbol = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return ('<Transaction {} Created At:{}>'.format(id, created_at))
