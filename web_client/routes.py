from flask import render_template, url_for, flash, redirect, request, session, jsonify,make_response
from web_client import db,app,bcrypt,intialize_firebase
from web_client.forms import RegistrationForm, LoginForm
from web_client.models import User
import json
from flask_login import login_user, current_user, logout_user, login_required
import requests
from datetime import datetime, timedelta
import jwt





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
    aapl_price = requests.get('http://localhost:5001/aapl/share_price').json()["Price"]
    # fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]
    # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]
    # goog_price = requests.get('http://localhost:5001/goog/price').json()["Price"]
     
    db.child("users").child("Morty").update({"name": "Mortiest Morty"})
   
    return render_template('dashboard.html', title='Dashboard', aapl_price=aapl_price, aapl_shares=aapl_shares)


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
    return token

@app.route("/addFunds", methods=["POST"])
def addFunds():
    # Retrieve amount and its in JSON form
    req = request.get_json()

    print ( str(current_user) + str(req))

    res = make_response(jsonify({"message": "OK"}), 200)

    return res
@app.route("/buy", methods=["POST"])
def buyShares():
     # Retrieve amount and its in JSON form
    req = request.get_json()

    print ( str(current_user) + str(req))

    res = make_response(jsonify({"message": "OK"}), 200)

    return res
@app.route("/sell", methods=["POST"])
def sellShares():
     # Retrieve amount and its in JSON form
    req = request.get_json()

    print ( str(current_user) + str(req))

    res = make_response(jsonify({"message": "OK"}), 200)

    return res