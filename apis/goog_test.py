from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta
from functools import wraps
import psycopg2
import requests
import unittest
import os
import sys
import jwt
from models.goog_table import updateMethods, insertMethods, checkMethods, create_bank_table
from goog_api import app, generate_token, get_price, token_check, buy_shares, sell_shares, showToken, get_quote


class TestGoogApi(unittest.TestCase):
    def test_check_share_price_route(self):
        c = app.test_client()
        response = c.get('/goog/share_price')
        self.assertEqual(response.status_code, 200)

    def test_check_buy_route(self):
        c = app.test_client()
        response = c.get('/goog/buy/')
        self.assertEqual(response.status_code, 200)

    def test_check_sell_route(self):
        c = app.test_client()
        response = c.get('/goog/sell/')
        self.assertEqual(response.status_code, 200)

    def test_check_shares_route(self):
        c = app.test_client()
        response = c.get('/goog/shares')
        self.assertEqual(response.status_code, 200)

    def test_generate_token(self):
        secret_key = os.getenv('welp')
        current_time = datetime.utcnow()

        test_toke1 = generate_token("TestUser")

        exp_time = current_time + timedelta(seconds=0, minutes=30, hours=0)
        test_load = {'username': "TestUser",
                     'exp': exp_time}

        test_toke2 = jwt.encode(
            test_load,
            key=str(secret_key),
            algorithm='HS256')

        decode_toke1 = jwt.decode(
            test_toke1,
            str(secret_key),
            algorithms='HS256')
        decode_toke2 = jwt.decode(
            test_toke2,
            str(secret_key),
            algorithms='HS256')

        self.assertEqual(decode_toke1['exp'], decode_toke2['exp'],
                         "Token expirations match")

        self.assertEqual(decode_toke1['username'], decode_toke2['username'],
                         "Token username match")

    def test_get_price(self):
        test_api_url = "https://sandbox.tradier.com/v1/markets/quotes"
        test_api_key = "Jo5Qmiac0PqN8dG360REQq8oGbNY"
        response = requests.get(
            test_api_url, params={
                'symbols': 'GOOGL'}, headers={
                'Accept': 'application/json', 'Authorization': 'Bearer ' + test_api_key})
        response = response.json()
        test_response1 = response['quotes']['quote']
        test_response2 = get_quote()

        self.assertEqual(test_response1['last'], test_response2['last'],
                         "get prices match")

    def test_database_connection(self):
        testConn = psycopg2.connect(
            'postgres://bdhcskpn:aN7RtxPZgnKxxjWBhOGzaSi5uVigON4l@salt.db.elephantsql.com:5432/bdhcskpn')
        if (testConn):
            pass


if __name__ == "__main__":
    unittest.main()
