from flask import render_template, url_for, flash, redirect, request, session, jsonify, make_response
from web_client import db, app, bcrypt, intialize_firebase
from web_client.forms import RegistrationForm, LoginForm
from web_client.models import User, Account
import json
import os
from flask_login import login_user, current_user, logout_user, login_required
import requests
from datetime import datetime, timedelta
import pyrebase
import jwt

dbfire = intialize_firebase().database()
uri_dict = {
    'AAPL': os.getenv("AAPL_URI"),
    'GOOG': os.getenv("GOOG_URI"),
    'FB': os.getenv("FB_URI"),
    'MSFT': os.getenv("MSFT_URI")}


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            token = generate_token(user.username)
            return redirect(url_for('home', token=json.dumps(
                {'token': token.decode('UTF-8')})))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
        # req = request.get_json()
    token = generate_token(current_user.username)
    aapl_shares = requests.get(
        'http://localhost:5001/aapl/share_amount',
        headers={
            'aapl_token': token}).json()["total_shares"]
    # print(aapl_shares)
    # print(req)
    aapl_price = requests.get(
        'http://localhost:5001/aapl/share_price').json()["Price"]
    # fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]
    # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]
    # goog_price = requests.get('http://localhost:5001/goog/price').json()["Price"]
    return render_template(
        'dashboard.html',
        title='Dashboard',
        aapl_price=aapl_price,
        aapl_shares=aapl_shares)

    # print(aapl_shares)


@app.route("/transactions")
@login_required
def transactions():
    return render_template('transactions.html', title='Transactions')
# Generates token


def generate_token(username, seconds=0, minutes=30, hours=0):

    exp_time = datetime.utcnow() + \
        timedelta(seconds=seconds, minutes=minutes, hours=hours)

    payload = {'username': username,
               'exp': exp_time
               }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode()


@app.route("/addFunds", methods=["POST"])
def addFunds():
    # Retrieve amount and its in JSON form
    req = request.get_json()

    print(str(current_user) + str(req))
    cash = (float)(req["fundAmount"])
    data = {
        "cash": cash
    }
    dbfire.child('transactions').child(
        current_user.username).child('funds').update(data)
    res = make_response(jsonify({"message": "OK"}), 200)

    return res


@app.route("/buy", methods=["POST"])
def buyShares():
     # Retrieve amount and its in JSON form
    req = request.get_json()

    print(str(current_user) + str(req))

    res = make_response(jsonify({"message": "OK"}), 200)

    return res


@app.route("/sell", methods=["POST"])
def sellShares():
     # Retrieve amount and its in JSON form
    req = request.get_json()

    if req is None:
        return jsonify({"message": "No sell amount provided"})

    try:

        sell_amount = req['sellAmount']
        symbol = req['symbol']
        if sell_amount <= 0 or symbol not in set('AAPL', 'GOOG', 'FB', 'MSFT'):
            raise Exception
    except Exception:
        return jsonify({"message": "invalid sell amount or symbol"})

    stock_uri = uri_dict[symbol]
    token = generate_token(current_user.username)
    headers = {"Token": token}

    current_account = Account.query.filter_by(
        account_name=req['account']).first()
    api_response = None

    if symbol == 'AAPL' and current_account.aapl_shares >= sell_amount:

        api_response = requests.post(url=stock_uri + '/sell', headers=headers)
        api_json = api_response.json()
        shares = api_json['shares_sold']
        payment = api_json['payment']
        current_account.aapl_shares = current_account.aapl_shares - shares
        current_account.cash = current_account.cash + payment

    elif symbol == 'FB' and current_account.fb_shares >= sell_amount:

        api_response = requests.post(url=stock_uri + '/sell', headers=headers)
        api_json = api_response.json()
        shares = api_json['shares_sold']
        payment = api_json['payment']
        current_account.aapl_shares = current_account.fb_shares - shares
        current_account.cash = current_account.cash + payment

    elif symbol == 'GOOG' and current_account.goog_shares >= sell_amount:

        api_response = requests.post(url=stock_uri + '/sell', headers=headers)
        api_json = api_response.json()
        shares = api_json['shares_sold']
        payment = api_json['payment']
        current_account.aapl_shares = current_account.goog_shares - shares
        current_account.cash = current_account.cash + payment

    elif symbol == 'MSFT' and current_account.msft_shares >= sell_amount:

        api_response = requests.post(url=stock_uri + '/sell', headers=headers)
        api_json = api_response.json()
        shares = api_json['shares_sold']
        payment = api_json['payment']
        current_account.aapl_shares = current_account.msft_shares - shares
        current_account.cash = current_account.cash + payment
    else:
        return jsonify({"message": "insufficent funds"})

    db.session.add(current_account)
    db.session.commit()

    return jsonify({"message": "success"})
