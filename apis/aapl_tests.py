import jwt
import unittest
import os
from aapl_helper import generate_token
from appl_api import aapl_price, aapl_api
import json
import dotenv
import requests
import multiprocessing
import time
dotenv.load_dotenv(dotenv_path=".{}config{}.env".format(os.sep, os.sep))


class TestAPI(unittest.TestCase):

    def test_share_price(self):
        api_url = "https://sandbox.tradier.com/v1/markets/quotes"

        params = {'symbols': 'AAPL'}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + os.getenv("AAPL_BEARER")
                   }

        price = aapl_price()['quotes']['quote']['last']

        response = requests.get(api_url, params=params, headers=headers)
        test_val = response.json()
        correctValue = round(test_val['quotes']['quote']['last'], 2)
        self.assertEqual(round(price, 2), correctValue)

    def test_aapl_buy(self):
        self.aapl_url = "http://localhost:5001"
        self.aapl_buy = "/aapl/buy/"
        token = generate_token("test")
        payload = {'amount': 200}
        headers = {"aapl_token": token}
        r = requests.get(
            self.aapl_url +
            self.aapl_buy,
            params=payload,
            headers=headers).json()
        self.assertEqual(r['symbol'], "AAPL")
        self.assertEqual(r['shares_bought'], '200')
        self.assertEqual(r['user'], 'test')

    def test_aapl_sell(self):
        self.aapl_url = "http://localhost:5001"
        self.aapl_sell = "/aapl/sell/"
        token = generate_token("test")
        payload = {'amount': 200}
        headers = {"aapl_token": token}
        r = requests.get(
            self.aapl_url +
            self.aapl_sell,
            params=payload,
            headers=headers).json()
        self.assertEqual(r['symbol'], "AAPL")
        self.assertEqual(r['shares_sold'], '200')
        self.assertEqual(r['user'], 'test')
    # def test_aapl_shares(self):
    #     self.aapl_url = "http://localhost:5001"
    #     self.aapl_shares = "/aapl/shares/"
    #     token = generate_token("test")
    #     headers = {"aapl_token": token}
    #     # payload = {'amount': 200}
    #     r = requests.get(
    #         self.aapl_url +
    #         self.aapl_shares,
    #         headers=headers).json()
    #     headers = {"aapl_token": token}
     
    #     # print(r['Total Shares'][0['symbol']])
    #     self.assertEqual(r['Total Shares'][0]['symbol'], 'AAPL')


if __name__ == "__main__":
    server = multiprocessing.Process(target=aapl_api.run, args=(None, 5001))
    server.start()
    time.sleep(2)
    unittest.main(exit=False)
    server.terminate()
    server.join()
