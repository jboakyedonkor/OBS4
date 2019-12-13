import unittest
import requests
import dotenv
from datetime import datetime, timedelta
import jwt
import pyrebase
import os
from multiprocessing import Process
from fb_api import app
from fb_api import get_token, token_verification, fire_db
import time


class FBRoutesTestCase(unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv(dotenv_path=r'.\\config\.env')
        self.secret_key = os.getenv('SECRET_KEY')
    #Unit
    def test_get_token(self):
        test_correct_token_header = {'token': '123'}
        test_incorrect_token_header = {'towkinz': '456'}

        correct_token = get_token(test_correct_token_header)
        incorrect_token = get_token(test_incorrect_token_header)

        self.assertEqual(correct_token, '123', 'Token not retrieved correctly')
        self.assertEqual(incorrect_token, None, 'Token did not send. Should not have returned token.')
    #Unit
    def test_token_verify(self):
        exp_time = datetime.utcnow() + timedelta(seconds=10)

        test_payload = {
            'username': 'test_user',
            'exp': exp_time
        }

        token = jwt.encode(test_payload, self.secret_key, algorithm='HS256')

        verify, decoded = token_verification(token)

        time.sleep(11)

        verify_2, decoded = token_verification(token)

        exp_time = datetime.utcnow() + timedelta(seconds=30)
        test_payload_2 = {
            'username': 'test_user',
            'exp': exp_time
        }

        token_3 = jwt.encode(test_payload, 'not_my_key', algorithm='HS256')
        
        verify_4, decoded = token_verification(token_3)

        self.assertEqual(verify, True, 'Token verification should return True.')
        self.assertEqual(verify_2, False, 'Token should have expired.')
        self.assertEqual(verify_4, False, 'Token should return invalid due to invalid signature.')
    #Unit
    def test_verify_user(self):
        payload = {'username': 'test_user',
                   'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, self.secret_key, algorithm='HS256')
        encoded_wrong_key = jwt.encode(payload, 'not_my_key', algorithm='HS256')

        res_no_token = requests.get(
            'http://localhost:5002/api/user/verify').json()
        self.assertEqual(
            res_no_token['authenticated'],
            False,
            'Authenticated when no token sent.')
        self.assertEqual(
            res_no_token['status'],
            400,
            'Did not respond with server error.')
        self.assertEqual(
            res_no_token['description'],
            'Token not received.',
            'Did not respond with correct error description.')

        res_token = requests.get(
            'http://localhost:5002/api/user/verify',
            headers={
                'token': encoded}).json()
        self.assertEqual(
            res_token['user'],
            'test_user',
            'Usernames does not match. User not authenticated.')
        self.assertEqual(res_token['status'], 200, 'Did not respond with server OK status.')
        self.assertEqual(res_token['description'], 'User is authenticated.', 'Did not respond with correct description.')
        self.assertEqual(res_token['authenticated'], True, 'Did not authenticate properly.')

        res_invalid_token = requests.get('http://localhost:5002/api/user/verify', headers={'token': encoded_wrong_key}).json()
        self.assertEqual(res_invalid_token['status'], 400, 'Did not respond with server error.')
        self.assertEqual(res_invalid_token['description'], 'User not authenticated', 'Did not respond with correct server description.')
        self.assertEqual(res_invalid_token['authenticated'], False, 'Did not authenticate properly.')
        self.assertEqual(res_invalid_token['user'], None, 'Did not respond with no user.')
    #Unit
    def test_get_price(self):
        res = requests.get('http://localhost:5002/fb/share_price').json()
        self.assertEqual(res['symbol'], 'FB', 'Incorrect symbol.')
        self.assertEqual(res['name'], 'Facebook Inc', 'Incorrect description.')
        self.assertIsInstance(
            res['Price'],
            float,
            'Incorrect data type. Should be float. Is ' +
            str(
                type(
                    res['Price'])))
    #Unit
    def test_create_transaction(self):
        trans_type = "TEST"
        payment = 2020
        price = 20
        username = 'fake_user'

        res_test = requests.post(
            'http://localhost:5002/api/transactions/FB',
            json={
                'trans_type': trans_type,
                'payment': payment,
                'price': price,
                'username': username},
            headers={
                'Content-Type': 'application/json'}).json()
        
        test_transaction = {
            'created_at': res_test['created_at'],
            'payment': 2020, 
            'share_price': 20,
            'symbol': 'FB',
            'username': username
        }

        res_bought = requests.post(
            'http://localhost:5002/api/transactions/FB',
            json={
                'trans_type': 'BUY',
                'payment': payment,
                'price': price,
                'username': username,
                'amount': 1},
            headers={
                'Content-Type': 'application/json'}).json()

        bought_transaction = {
            'created_at': res_bought['created_at'],
            'payment': 2020, 
            'share_price': 20,
            'symbol': 'FB',
            'username': username,
            'shares_bought': 1
        }

        res_sold = requests.post(
            'http://localhost:5002/api/transactions/FB',
            json={
                'trans_type': 'SELL',
                'payment': payment,
                'price': price,
                'username': username,
                'amount': 1},
            headers={
                'Content-Type': 'application/json'}).json()

        sold_transaction = {
            'created_at': res_sold['created_at'],
            'payment': 2020, 
            'share_price': 20,
            'symbol': 'FB',
            'username': username,
            'shares_sold': 1
        }

        self.assertEqual(res_test, test_transaction, 'Route did not return transaction properly.')
        self.assertEqual(res_bought, bought_transaction, 'Route did not return transaction properly.')
        self.assertEqual(res_sold, sold_transaction, 'Route did not return transaction properly.')
    #Unit
    def test_buy_share(self):
        username = 'fake_user'
        secret = self.secret_key
        payload = {'username': username,
                   'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, secret, algorithm='HS256')

        res = requests.post(
            'http://localhost:5002/fb/buy',
            headers={
                'Content-Type': 'application/json',
                'token': encoded},
            json={
                'amount': 400}).json()

        expected_res = {
            'user': username,
            'symbol': 'FB',
            'share_price': res['share_price'],
            'shares_bought': 400,
            'created_at': res['created_at'],
            'payment': 400 * res['share_price']
        }

        self.assertEqual(res, expected_res, 'Did not return bought transaction properly.')
        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')
    #Unit
    def test_sell_share(self):
        username = 'fake_user'
        secret = self.secret_key
        payload = {'username': username,
                   'exp': datetime.utcnow() + timedelta(minutes=30)}
        encoded = jwt.encode(payload, secret, algorithm='HS256')

        res = requests.post(
            'http://localhost:5002/fb/sell',
            headers={
                'Content-Type': 'application/json',
                'token': encoded},
            json={
                'amount': 400}).json()

        expected_res = {
            'user': username,
            'symbol': 'FB',
            'share_price': res['share_price'],
            'shares_sold': 400,
            'created_at': res['created_at'],
            'payment': 400 * res['share_price']
        }

        self.assertEqual(res, expected_res, 'Did not return sold transaction correctly.')
        self.assertIsNotNone(res, 'Route did not return anything.')
        self.assertIsInstance(res, dict, 'Did not return valid json.')

    def tearDown(self):
        fire_db.child('transactions').child('fake_user').remove()


if __name__ == '__main__':
    # server = Process(target=app.run)
    # server.start()
    # time.sleep(2)
    unittest.main(exit=False)
    # server.terminate()
    # server.join()
