import requests, json
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

#api = Blueprint()
app = Flask(__name__)

@app.route('/msft/buy',methods=['POST'])
def buy_share():
    return True

@app.route('/msft/sell',methods=['POST'])
def sell_share():
    return True

@app.route('/msft/share_price',methods=['GET'])
def get_price():
    return True

@app.route('/msft/shares',methods=['GET'])
def get_shares():
    return True

if __name__ == "__main__":
    app.run() 