import unittest
from routes import generate_token
import jwt
class TestUserModel(unittest.TestCase):
    def test_split(self):
        username ='test'
        email='test@test.com'
        password='test'
        user = User(
            username =username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()
        auth_token = generate_token(username);
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(auth_token.decode('UTF-8') == 1)
    
    
# if __name__ == '__main__':
#     unittest.main()