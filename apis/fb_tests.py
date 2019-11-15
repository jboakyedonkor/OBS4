import unittest
import requests
import dotenv
from datetime import datetime, timedelta
import jwt
import pyrebase
import os

class FBRoutesTestCase(unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv(dotenv_path='.\\config\.env')
    
    def test_verify_user(self):
        username = 'fakeemail@faketaxi.com'
        secret = os.getenv('SERVER_KEY')
        payload = {'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, secret, algorithm='HS256')

        res_no_token = requests.get('http://localhost:5000/api/user/verify').json()
        self.assertEqual(res_no_token['authenticated'], False, 'Authenticated when no token sent.')

        res_token = requests.get('http://localhost:5000/api/user/verify', headers={'token': encoded}).json()
        self.assertEqual(res_token['user'], username, 'Usernames does not match. User not authenticated.')
        self.assertIsInstance(res_token, dict, 'Did not return valid json.')
    
    def test_get_price(self):
        res = requests.get('http://localhost:5000/fb/share_price').json()
        self.assertEqual(res['symbol'], 'FB', 'Incorrect symbol.')
        self.assertEqual(res['name'], 'Facebook Inc', 'Incorrect description.')
        self.assertIsInstance(res['share_price'], float, 'Incorrect data type. Should be float. Is ' + str(type(res['share_price'])))

    def test_create_transaction(self):
        trans_type = "TEST"
        amount = 101
        price = 20
        username = 'fakeemail@faketaxi.com'

        res = requests.post('http://localhost:5000/api/transactions/FB', 
                            json={'trans_type': trans_type, 'amount': amount, 'price': price, 'username': username},
                            headers={'Content-Type': 'application/json'}).json()

        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')

    def test_get_transactions(self):
        res = requests.get('http://localhost:5000/api/transactions/admin/FB').json()
        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')

    def test_buy_share(self):
        username = 'fakeemail@faketaxi.com'
        secret = os.getenv('SERVER_KEY')
        payload = {'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, secret, algorithm='HS256')

        res = requests.post('http://localhost:5000/fb/buy',
                            headers={'Content-Type': 'application/json', 'token': encoded},
                            json={'amount': 400, 'username': username}).json()
        
        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')

    def test_sell_share(self):
        username = 'fakeemail@faketaxi.com'
        secret = os.getenv('SERVER_KEY')
        payload = {'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, secret, algorithm='HS256')

        res = requests.post('http://localhost:5000/fb/sell',
                            headers={'Content-Type': 'application/json', 'token': encoded},
                            json={'amount': 400, 'username': username}).json()

        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')

if __name__ == '__main__':
    unittest.main(exit=False)