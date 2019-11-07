"""Modules include time formatting, http requests, pyjwt for token authentication
and secret key storage."""
from datetime import datetime
import requests
import jwt
import keys


def get_price():
    """This function fetches the price of a Facebook stock."""
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                            params={'symbols': 'FB', 'greeks': 'false'},
                            headers={'Authorization': keys.get_auth_key(),
                                     'Accept': 'application/json'})

    response_json = response.json()
    return response_json['quotes']['quote']['last']


def verify(token=keys.get_jwt_key()):
    """This function verifies the authentication token."""
    # The token will need a user account unique identifier and current login credentials
    # The payload for the jwt will be { 'user_id', 'password' }
    # with headers { 'login_time', 'token_expire' }
    if token is None:
        raise Exception('Authentication token does not exist.')

    decoded = jwt.decode(token, keys.get_secret(), algorithm='HS256')

    if datetime.strptime(decoded['token_expire'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():
        raise Exception('Authentication token has expired.')

    return bool(decoded['password'] == keys.get_password())

print(verify())