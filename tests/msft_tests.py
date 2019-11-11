
import datetime
from subprocess import Popen
import requests
import os
import sys
import time
import unittest
import dotenv
import jwt
from flask import Flask
sys.path.append(os.getcwd())
from stockAPIs.msft_api import generate_token, verify_token, get_quote, get_token

class MsftHelperTestCase (unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv(
            dotenv_path=".{}config{}.env".format(
                os.sep, os.sep))
        self.secret_key = os.getenv('SECRET_KEY')
        self.api_key = os.getenv('API_KEY')

    def test_get_quote(self):
        api_url = "https://sandbox.tradier.com/v1/markets/quotes"

        params = {'symbols': 'MSFT'}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.api_key
                   }

        api_response = get_quote()

        test_response = requests.get(api_url, params=params, headers=headers)
        test_json = test_response.json()

        self.assertEqual(
            api_response,
            test_json['quotes']['quote'],
            "the Tradier API do not get the same response")

    def test_get_token(self):
        test_header = {'Authorization': 'check'}
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

    def test_generate_token(self):

        token = generate_token("test", self.secret_key, seconds=10, minutes=0)
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)

        test_payload = {

            'username': "test",
            'iss': 'Microsoft_API',
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
            decoded_test_token['iss'],
            decoded_token['iss'],
            "invalid issuer")

        self.assertEqual(
            decoded_test_token['exp'],
            decoded_token['exp'],
            "Not a close enough expiration time")

    def test_verify_token(self):

        exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        test_payload = {

            'username': "test",
            'iss': 'Microsoft_API',
            'exp': exp_time
        }

        token = jwt.encode(
            test_payload,
            self.secret_key,
            algorithm='HS256')

        output = verify_token(token, self.secret_key)

        time.sleep(11)

        output2 = verify_token(token, self.secret_key)

        exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        test_payload2 = {

            'username': "test",
            'iss': 'Micrsosoft_API',
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

        # checks invalid issuer
        self.assertEqual(output3, (False, 'invalid iss'),
                         "token should have been rejected as invalid issuer")
        # checks for invalid signature
        self.assertEqual(output4, (False, "invalid signature"),
                         "should have been rejected as an invalid signature")


class MsftRoutesTestCase(unittest.TestCase):

    def test_get_shares(self):
        pass

    def test_get_price(self):
        pass

    def test_post_buy(self):
        pass

    def test_post_sell(self):
        pass


if __name__ == "__main__":

    cmd = ['python3', '.' + os.sep + 'StockAPIs' + os.sep + 'msft_api.py']

    if os.name == 'nt':
        cmd[0] = 'python'

    api_proc = Popen(cmd)
    time.sleep(0.7)
    unittest.main(exit=False, verbosity=3)
    api_proc.kill()
    time.sleep(0.2)
