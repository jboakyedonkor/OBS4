from subprocess import Popen
import requests
import os
import time
import unittest
from flask import Flask


class MsftTestCase (unittest.TestCase):

    def test_get_shares(self):
        pass

    def test_get_price(self):
        pass

    def test_post_buy(self):
        pass

    def test_post_sell(self):
        pass


if __name__ == "__main__":

    cmd = ['python3', '..' + os.sep + 'StockAPIs' + os.sep + 'msft_api.py']
    api_proc = Popen(cmd)
    time.sleep(0.2)
    unittest.main(exit=False)
    api_proc.kill()
    time.sleep(0.2)
