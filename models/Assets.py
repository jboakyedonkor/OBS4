from server import ma, db

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