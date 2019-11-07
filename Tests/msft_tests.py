from subprocess import Popen
import requests ,os , time, unittest,signal
#from StockAPIs.msft_api import microsoft_api
from flask import Flask
import os


class MsftTestCase (unittest.TestCase):

    def setUp(self):
        filepath = '..'+os.sep+'StockAPIs'+os.sep+'msft_api.py'
        cmd = ['python3',filepath]
        if os.name == 'nt':
            cmd[0] = 'python'

        self.api_process = Popen(cmd,shell = True)
        time.sleep(0.1)
        print("started ") 
    
    def test_function(self):
        tg=requests.get('http://localhost:5000/msft/sell')
        print(tg.text)
        self.assertEqual(True, True,'dsd')
    def tearDown(self):
        status = Popen.poll(self.api_process)
        print(status)
        while status == None:
            self.api_process.kill()
            time.sleep(0.5)
        
if __name__ == "__main__":
    unittest.main()