from app import app
from app.apis.appl_api import aapl_api
from app.apis.fb_api import facebook_api


app.register_blueprint(aapl_api)
app.register_blueprint(facebook_api)


if __name__ == '__main__':
    app.run(debug=True)