from app import app
from app.stockAPIs.appl_api import aapl_api



app.register_blueprint(aapl_api)

if __name__ == '__main__':
    app.run(debug=True)