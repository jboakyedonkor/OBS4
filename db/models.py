from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock (db.Model):
    self.id = db.Column(db.Integer, primary_key = True)
    self.symbol = db.Column(db.String(20),nullable = False)
    self.price = db.Column(db.Float, nullable = False)
    self.shares =db.Column(db.Integer , nullable = False)
    
    def __repr__():
        