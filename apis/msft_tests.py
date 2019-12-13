import requests
import os
import time
import unittest
import dotenv
import jwt
from multiprocessing import Process
from datetime import datetime, timedelta
from msft_helpers import *
from msft_api import microsoft_api


class MsftHelperTestCase (unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv(
            dotenv_path=".{}config{}.env".format(
                os.sep, os.sep))
        self.secret_key = os.getenv('SECRET_KEY')
        self.api_key = os.getenv('MSFT_TRADIER_API_KEY')
    #Unit
    def test_get_quote(self):
        api_url = "https://sandbox.tradier.com/v1/markets/quotes"

        params = {'symbols': 'MSFT'}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.api_key
                   }

        api_response = get_quote()

        test_response = requests.get(api_url, params=params, headers=headers)
        test_json = test_response.json()

        # self.assertEqual(
        #     api_response['symbol'],
        #     test_json['quotes']['quote']['symbol'],
        #     "not the same company")

        self.assertEqual(
            api_response['description'],
            test_json['quotes']['quote']['description'],
            "not the same company")
    #Unit
    def test_get_token(self):
        test_header = {'token': 'check'}
        test_header2 = {'Authorizationd': 'check'}

        token = get_token(test_header)
        token2 = get_token(test_header2)

        self.assertEqual(
            token,
            'check',
            'the authorization shoud be \'check\'')

        self.assertEqual(
            token2,
            None,
            'The was not authorization header or an empty header')
    #Unit
    def test_generate_token(self):

        token = generate_token("test", self.secret_key, seconds=10, minutes=0)
        exp_time = datetime.utcnow() + timedelta(seconds=10)

        test_payload = {

            'username': "test",
            'exp': exp_time
        }

        test_token = jwt.encode(
            test_payload,
            self.secret_key,
            algorithm='HS256')

        decoded_token = jwt.decode(token, self.secret_key, algorithms='HS256')
        decoded_test_token = jwt.decode(
            test_token, self.secret_key, algorithms='HS256')

        self.assertEqual(
            decoded_test_token['username'],
            decoded_token['username'],
            "username is not the same")

        self.assertEqual(
            decoded_test_token['exp'],
            decoded_token['exp'],
            "Not a close enough expiration time")
    #Unit
    def test_verify_token(self):

        exp_time = datetime.utcnow() + timedelta(seconds=10)
        test_payload = {

            'username': "test",
            'exp': exp_time
        }

        token = jwt.encode(
            test_payload,
            self.secret_key,
            algorithm='HS256')

        output = verify_token(token, self.secret_key)

        time.sleep(11)

        output2 = verify_token(token, self.secret_key)

        exp_time = datetime.utcnow() + timedelta(seconds=30)
        test_payload2 = {

            'username': "testuser",
            'exp': exp_time
        }

        token2 = jwt.encode(
            test_payload2,
            self.secret_key,
            algorithm='HS256')

        token3 = jwt.encode(
            test_payload,
            'invalid_key',
            algorithm='HS256'
        )
        output3 = verify_token(token2, self.secret_key)
        output4 = verify_token(token3, self.secret_key)

        # checks for valid signature
        self.assertEqual(output, (True, "test"),
                         "output show be a True \"test\" ")

        # checks for token expiration
        self.assertEqual(output2, (False, "token expired"),
                         " token show have expired")

        # checks for invalid signature
        self.assertEqual(output4, (False, "invalid signature"),
                         "should have been rejected as an invalid signature")


class MsftRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.msft_url = "http://localhost:5003"
        self.price_route = "/msft/share_price"
        self.buy_route = "/msft/buy"
        self.sell_route = "/msft/sell"

        dotenv.load_dotenv(
            dotenv_path=".{}config{}.env".format(
                os.sep, os.sep))
        self.secret_key = os.getenv('SECRET_KEY')
        self.api_key = os.getenv('MSFT_TRADIER_API_KEY')
    #Unit
    def test_get_price(self):
        token = generate_token('testuser', self.secret_key)
        headers = {'token': token.decode()}
        api_response = requests.get(
            self.msft_url + self.price_route,
            headers=headers).json()

        token2 = generate_token(
            'testuser',
            self.secret_key,
            seconds=1,
            minutes=0)
        time.sleep(2)
        headers = {'token': token2.decode()}
        api_response2 = requests.get(
            self.msft_url + self.price_route,
            headers=headers).json()

        api_response3 = requests.get(
            self.msft_url + self.price_route).json()

        self.assertEqual(
            api_response3['error'],
            "Invalid token",
            "incorrect error response")

        self.assertEqual(
            api_response['symbol'],
            'MSFT',
            'incorrect user made a requests')
        self.assertEqual(
            api_response['name'],
            'Microsoft Corp',
            'incorrect company')

        self.assertEqual(
            api_response2['error'],
            "token expired",
            "incorrect error response")
    #Unit
    def test_post_buy(self):

        token = generate_token('testuser', self.secret_key)

        headers = {'token': token.decode()}
        json_data = {'shares': 45}

        api_response = requests.post(
            self.msft_url + self.buy_route,
            json=json_data,
            headers=headers).json()

        token2 = generate_token(
            'testuser',
            self.secret_key,
            seconds=1,
            minutes=0)

        time.sleep(2)

        headers = {'token': token2.decode()}

        api_response2 = requests.post(
            self.msft_url + self.buy_route,
            json=json_data,
            headers=headers).json()

        api_response3 = requests.post(
            self.msft_url + self.buy_route).json()

        api_response4 = requests.post(
            self.msft_url + self.buy_route,
            headers={
                'token': '223443dd'}).json()

        self.assertEqual(
            ('error' in api_response4.keys()),
            True,
            "should not valid")

        self.assertEqual(
            api_response3['error'],
            "Invalid token",
            "incorrect error response")

        self.assertEqual(
            api_response['shares_bought'],
            45,
            "incorrect amount shares sold")

        self.assertEqual(api_response['symbol'], 'MSFT', 'incorrect quote')

        self.assertEqual(
            api_response['payment'],
            api_response['shares_bought'] *
            api_response['share_price'] * -1,
            "incorrect payment")

        self.assertEqual(
            api_response2['error'],
            "token expired",
            "incorrect error response")
    #Unit
    def test_post_sell(self):
        token = generate_token('testuser', self.secret_key)

        headers = {'token': token.decode()}
        json_data = {'shares': 45}

        api_response = requests.post(
            self.msft_url + self.sell_route,
            json=json_data,
            headers=headers).json()

        token2 = generate_token(
            'testuser',
            self.secret_key,
            seconds=1,
            minutes=0)

        time.sleep(2)

        headers = {'token': token2.decode()}

        api_response2 = requests.post(
            self.msft_url + self.sell_route,
            json=json_data,
            headers=headers).json()

        api_response3 = requests.post(
            self.msft_url + self.sell_route).json()

        api_response4 = requests.post(
            self.msft_url + self.sell_route,
            headers={
                'token': '223443dd'}).json()

        self.assertEqual(
            ('error' in api_response4.keys()),
            True,
            "should not valid")

        self.assertEqual(
            api_response3['error'],
            "Invalid token",
            "incorrect error response")
        self.assertEqual(
            api_response['shares_sold'],
            45,
            "incorrect amount shares bought")

        self.assertEqual(api_response['symbol'], 'MSFT', 'incorrect quote')

        self.assertEqual(
            api_response['payment'],
            api_response['shares_sold'] *
            api_response['share_price'],
            "incorrect payment")

        self.assertEqual(
            api_response2['error'],
            "token expired",
            "incorrect error response")


if __name__ == "__main__":

    server = Process(target=microsoft_api.run,args=(None,5003))
    server.start()

    time.sleep(4)
    unittest.main(exit=False, verbosity=3)

    server.terminate()
    server.join()

    time.sleep(4)

    db = create_firebase_app()
    if db:
        db = db.database()
        db.child("transcations").child("testuser").remove()
