import requests, json
from flask import Flask, Blueprint
#from flask_sqlalchemy import SQLAlchemy

microsoft_api= Blueprint('microsoft_api',__name__)


@microsoft_api.route('/msft/buy',methods=['POST'])
def buy_share():
    return '/msft/buy'

@microsoft_api.route('/msft/sell',methods=['POST'])
def sell_share():
    return '/msft/sell'

@microsoft_api.route('/msft/share_price',methods=['GET'])
def get_price():
    return '/msft/share_price'

@microsoft_api.route('/msft/shares',methods=['GET'])
def get_shares():
    return '/msft/shares'

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(microsoft_api)
    app.run()