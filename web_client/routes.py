from flask import render_template, url_for, flash, redirect, request, session, jsonify, make_response
from web_client import db, app, bcrypt, intialize_firebase
from web_client.forms import RegistrationForm, LoginForm
from web_client.models import User
from web_client.username_table import *
import time
import json
from flask_login import login_user, current_user, logout_user, login_required
import requests
from datetime import datetime, timedelta
import jwt


#put apis here, or uncomment from the dashboard function
aapl_price = 270.0
fb_price = 202.0
msft_price = 151.0
goog_price = 1300.0


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
        signOutUsers()
        savedUser = str(form.username.data)
        time.sleep(2)
        insert_user_table(savedUser, savedUser, "0", "Y", "0", "0", "0", "0")

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

            updateSignIn("Y", str(current_user.username), str(current_user.username))

            return redirect(url_for('home', token=json.dumps(
                {'token': token.decode('UTF-8')})))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    signOutUsers()
    time.sleep(2)
    logout_user()
    return redirect(url_for('login'))


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    # req = request.get_json()
    token = generate_token(current_user.username)
    # print(str(current_user.username) + "dashboard username")

    # aapl_shares = requests.get('http://localhost:5001/aapl/share_amount',headers={'aapl_token': token}).json()["total_shares"]

    #aapl_price2 = requests.get('http://localhost:5001/aapl/share_price').json()["Price"]
    print("yeet")
    #print(aapl_price2)
    # fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]
    # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]
    #goog_price = requests.get('http://localhost:5001/goog/price').json()["Price"]

    return render_template('dashboard.html', title='Dashboard',
                           user_networth=str(getUserNetworth(str(current_user.username), aapl_price,
                                                             fb_price, msft_price, goog_price)),
                           aapl_price=aapl_price,
                           goog_price=goog_price,
                           msft_price=msft_price,
                           fb_price=fb_price,
                           accountNum=getUserAccounts(str(current_user.username)),
                           user_funds=getPrevFunds(str(current_user.username), returnAccount()),
                           goog_share_num=getShareNum(str(current_user.username), returnAccount(), "googl"),
                           aapl_share_num=getShareNum(str(current_user.username), returnAccount(), "aapl"),
                           fb_share_num=getShareNum(str(current_user.username), returnAccount(), "fb"),
                           msft_share_num=getShareNum(str(current_user.username), returnAccount(), "msft")
                           )


@app.route("/transactions")
@login_required
def transactions():
    return render_template('transactions.html', title='Transactions')


def generate_token(username, seconds=0, minutes=30, hours=0):
    exp_time = datetime.utcnow() + \
               timedelta(seconds=seconds, minutes=minutes, hours=hours)

    payload = {'username': username,
               'exp': exp_time
               }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def returnAccount():
    return getAccUser("Y")


@app.route("/getUser", methods=["POST"])
def getUser():
    req = request.get_json()

    savedUser = str(current_user.username)

    signOutUsers()
    time.sleep(2)
    updateSignIn("Y", savedUser, str(req))
    res = make_response(jsonify({"message": "OK"}), 200)
    return res


@app.route("/addFunds", methods=["POST"])
def addFunds():
    # Retrieve amount and its in JSON form
    req = request.get_json()

    insertFunds(str(current_user.username), returnAccount(), str(req["fundAmount"]))

    res = make_response(jsonify({"message": "OK"}), 200)

    return res


@app.route("/addAccount", methods=["POST"])
def addAccount():
    req = request.get_json()

    savedUser = str(current_user.username)
    savedAcc = str(req['newAccount'])
    accCount = (accNum(savedUser))

    if (accCount <= 2 and accCount > 0):
        signOutUsers()
        insert_user_table(savedUser, savedAcc, "0", "Y", "0", "0", "0", "0")
        res = make_response(jsonify({"message": "OK"}), 200)
    else:
        res = make_response(jsonify({"message": "Err - no more than 3 accounts"}), 200)
    return res


@app.route("/buy", methods=["POST"])
def buyShares():
    # Retrieve amount and its in JSON form
    req = request.get_json()
    token = generate_token(current_user.username)
    headers = {'token': token}

    buyAmount = (float)(req["buyAmount"])  # probably want float but dont know how your sql works
    # print(buyAmount)
    symPass = str(req["Symbol"])
    data = {'amount': buyAmount}
    finalFund = (getPrevFunds(str(current_user.username), returnAccount()))
    cash = (float)(finalFund)

    # retrieve cash in account if symbol is AAPL and buyAmount *appl_shares < cash then store
    if (symPass == 'aapl'):
        #aapl_price = requests.get('http://localhost:5001/aapl/share_price').json()["Price"]
        tot = buyAmount * aapl_price
        if (tot < cash):
            updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)
            # print(tot)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    if (symPass == 'msft'):
        # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]
        tot = buyAmount * msft_price
        if (tot < cash):
            updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)
            # print(tot)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    if (symPass == 'fb'):
        # fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]
        tot = buyAmount * fb_price
        if (tot < cash):
            updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)
            # print(tot)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    if (symPass == 'googl'):
        # goog_price = requests.get('http://localhost:5001/goog/share_price').json()["Price"]
        tot = buyAmount * goog_price
        if (tot < cash):
            updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    res = make_response(jsonify({"message": "OK"}), 200)
    return res


@app.route("/sell", methods=["POST"])
def sellShares():
    # Retrieve amount and its in JSON form
    req = request.get_json()
    token = generate_token(current_user.username)
    headers = {'token': token}

    sellAmount = (float)(req["sellAmount"])
    symPass = str(req["Symbol"])
    data = {'amount': sellAmount}

    tot_shares = (getShareNum(str(current_user.username), returnAccount(), symPass))

    if (symPass == 'aapl'):
        #aapl_price = requests.get('http://localhost:5001/aapl/share_price').json()["Price"]

        tot = sellAmount * aapl_price
        # add tot to cash val
        # subtract from appl shares
        # get current amount of appl shares and check if you are trying to sell less then the one you have
        if (sellAmount <= tot_shares):
            updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)

            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    if (symPass == 'msft'):
        # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]

        tot = sellAmount * msft_price
        # add tot to cash val
        # subtract from appl shares
        # get current amount of appl shares and check if you are trying to sell less then the one you have
        if (sellAmount <= tot_shares):
            updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    if (symPass == 'fb'):
        # fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]

        tot = sellAmount * fb_price
        # add tot to cash val
        # subtract from appl shares
        # get current amount of appl shares and check if you are trying to sell less then the one you have
        if (sellAmount <= tot_shares):
            updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)

            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    if (symPass == 'googl'):
        # goog_price = requests.get('http://localhost:5001/goog/share_price').json()["Price"]

        tot = sellAmount * goog_price
        # add tot to cash val
        # subtract from appl shares
        # get current amount of appl shares and check if you are trying to sell less then the one you have
        if (sellAmount <= tot_shares):
            updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

            res = make_response(jsonify({"message": "OK"}), 200)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            return res


    res = make_response(jsonify({"message": "OK"}), 200)
    return res
