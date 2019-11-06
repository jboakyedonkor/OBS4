import requests
import keys

def get_fb_price():
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params = {'symbols': 'FB', 'greeks': 'false'},
        headers = {'Authorization': keys.get_auth_key(), 'Accept': 'application/json'})

    response_json = response.json()
    return response_json['quotes']['quote']['last']

print(get_fb_price())