from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String)

    def __init__(self, email, password, token):
        self.email = email
        self.password = password
        self.token = token

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'email', 'password', 'token')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class FBTransaction(db.Model):
    trans_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    trans_type = db.Column(db.String(4))
    price = db.Column(db.Float)
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'))
    user = db.relationship('User', backref='fbtransactions')

    def __init__(self, timestamp, amount, trans_type, price, user_id):
        self.timestamp = timestamp
        self.amount = amount
        self.trans_type = trans_type
        self.price = price
        self.user_id = user_id

class FBTransactionSchema(ma.Schema):
    class Meta:
        fields = ('trans_id', 'timestamp', 'amount', 'trans_type', 'price', 'user_id')

transaction_FB_schema = FBTransactionSchema()
transactions_FB_schema = FBTransactionSchema(many=True)

class Asset(db.Model):
    asset_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(4))
    pl = db.Column(db.Float)
    num_owned = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', backref='assets')

    def __init__(self, symbol, pl, num_owned, user_id):
        self.symbol = symbol
        self.pl = pl
        self.num_owned = num_owned
        self.user_id = user_id

class AssetSchema(ma.Schema):
    class Meta:
        fields = ('asset_id', 'symbol', 'pl', 'num_owned', 'user_id')
        
asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)