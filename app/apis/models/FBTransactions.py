from fb_api import db, ma

class FBTransaction(db.Model):
    trans_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    trans_type = db.Column(db.String(4))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
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