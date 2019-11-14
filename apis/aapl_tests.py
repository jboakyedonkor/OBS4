import unittest
import os
from 
from web_client import app,db
from web_client.models import User
from web_client.routes import generate_token
import jwt

class TestUserModel(unittest.TestCase):
  
    def test_user(self):
        username ='test4'
        email='test4@test.com'
        password='test'
        user = User(
            username =username,
            email=email,
            password=password
    )
        user2 = User.query.filter_by(email=email).first()
        # For testing Checks if username is already in database and if so then delete then reinsert
        if(user2 != None):
            db.session.delete(user2)
            db.session.commit()
            db.session.add(user)
            db.session.commit()
        else:
            db.session.add(user)
            db.session.commit()
        
       
        
        auth_token = generate_token(username);
        self.assertTrue(isinstance(auth_token, bytes))
        
    def test_auth(self):
        username ='test4'
        email='test4@test.com'
        password='test'
        auth_token = generate_token(username);
        decoded = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms='HS256')
        print(decoded)
        self.assertTrue(decoded['username'] == 'test4')
        

if __name__ == "__main__":
    unittest.main()