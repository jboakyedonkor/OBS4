from subprocess import Popen
import requests
import os
import time
import unittest
import dotenv
import jwt
from flask import Flask
from stockAPIs.msft_api import generate_token, verify_token
import datetime


class MsftTestCase (unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv(
            dotenv_path=".{}config{}.env".format(
                os.sep, os.sep))
        self.secret_key = os.getenv('SECRET_KEY')
        self.api_key = os.getenv('API_KEY')

    def test_get_shares(self):
        pass

    def test_get_price(self):
        pass

    def test_post_buy(self):
        pass

    def test_post_sell(self):
        pass

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

        decoded_token = jwt.decode(token, self.secret_key)
        decoded_test_token = jwt.decode(test_token, self.secret_key)

        self.assertEqual(
            decoded_test_token['username'],
            decoded_token['username'],
            "username is not the same")

        self.assertEqual(
            decoded_test_token['iss'],
            decoded_token['iss'],
            "invalid issuer")

        self.assertAlmostEqual(
            decoded_test_token['exp'],
            decoded_token['exp'],
            "Not a close enough expiration time")

    def test_verify_token(self):
        pass


if __name__ == "__main__":
    
    cmd = ['python3', '..' + os.sep + 'StockAPIs' + os.sep + 'msft_api.py']
    api_proc = Popen(cmd)
    time.sleep(0.2)
    unittest.main(exit=False)
    api_proc.kill()
    time.sleep(0.2)
