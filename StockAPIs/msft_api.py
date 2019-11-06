import requests, json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DATA']

@app.route('/msft/buy',methods=['POST'])
def buy_share():
    pass

@app.route('/msft/sell',methods=['POST'])
def sell_share():
    pass

@app.route('/msft/share_price',methods=['GET'])
def get_price():
    pass

@app.route('/msft/shares',methods=['GET'])
def get_shares():
    pass