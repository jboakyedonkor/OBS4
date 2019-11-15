import unittest
import requests
import dotenv
from datetime import datetime, timedelta
import jwt
import pyrebase

class FBRoutesTestCase(unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv(dotenv_path='.\\config\.env')
    
    def test_verify_user(self):
        username = 'fakeemail@faketaxi.com'
        secret = os.getenv('SERVER_KEY')
        payload = {'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, seceret, algorithm='HS256')

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

        config = {
            "apiKey": os.getenv('FIREBASE_API_KEY'),
            "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
            "databaseURL": os.getenv('FIREBASE_DB_URL'),
            "projectId": os.getenv('FIREBASE_PROJECT_ID'),
            "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
            "messagingSenderId": os.getenv('FIREBASE_MSG_SENDER_ID'),
            "appId": os.getenv('FIREBASE_APP_ID'),
            "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
        }

        fire_db = pyrebase.initialize_app(config).database()

        try:
            test_transaction = fire_db.child('transactions').order_by_child('username').equal_to(username).get().val()
            test_transaction_info = list(test_transaction.items())[0][1]
        except:
            test_transaction_info = None

        self.assertIs(res, test_transaction_info, 'Transaction information did not save correctly.')
        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')

    def test_get_transactions(self):
        res = requests.get('http://localhost:5000/api/transactions/admin/FB').json()
        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')
        