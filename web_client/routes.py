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
import pyrebase

fire_db = intialize_firebase().database()
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
            login_user(user)
            data ={
            "email": form.email.data,
            "status": "Success",
            "time": str(datetime.utcnow())
            }
            fire_db.child('AUTH').child(str(user.username)).push(data)

            token = generate_token(user.username)
            return redirect(url_for('home', token=json.dumps(
                {'token': token.decode('UTF-8')})))
        else:
            data ={
            "email": form.email.data,
            "status": "Failure",
            "time": str(datetime.utcnow())
            }
            email = str(user.username)
            fire_db.child('AUTH').child(email).push(data)
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    signOutUsers()
    time.sleep(2)
    username = str(current_user.username)
    data ={
            "user":username,
            "status": "Logout",
            "time": str(datetime.utcnow())
            }
    
    fire_db.child('AUTH').child(username).push(data)
    logout_user()
    return redirect(url_for('login'))


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    token = generate_token(current_user.username)
    # aapl_shares = requests.get('http://localhost:5001/aapl/share_amount',headers={'token': token}).json()["total_shares"]
    aapl_price = requests.get('http://localhost:5001/aapl/share_price').json()["Price"]
    # fb_price = requests.get('http://localhost:5002/fb/share_price').json()["Price"]
    # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]
    # goog_price = requests.get('http://localhost:5001/goog/price').json()["Price"]
    # return render_template('dashboard.html', title='Dashboard', aapl_price=aapl_price, fb_price=fb_price)
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


@app.route("/logs")
@login_required
def transactions():
    all_transactions = requests.get('http://localhost:5000/transaction_parse').json()
    all_auth_log = requests.get('http://localhost:5000/auth_parse').json()
    all_obs_log = requests.get('http://localhost:5000/obs_parse').json()
    return render_template('transactions.html', title='Logs', all_transactions=all_transactions, auth_log=all_auth_log, obs_log=all_obs_log)

@app.route('/auth_parse', methods=["GET", "POST"])
def parse_auth():
    auth_log = requests.get('http://localhost:5000/api/auth/admin').json()
    present_auth = []

    for user_value in auth_log.values():
        for trans in user_value.values():
            present_auth.append(trans)
    
    return jsonify(sorted(present_auth, key=lambda i: i["time"], reverse=True))

@app.route('/obs_parse', methods=['GET', 'POST'])
def parse_obs():
    obs_log = requests.get('http://localhost:5000/api/obs/admin').json()
    present_obs = []

    for user_value in obs_log.values():
        for obs in user_value.values():
            present_obs.append(obs)

    return jsonify(sorted(obs_log, key=lambda i: i["time"], reverse=True))

@app.route('/api/auth/admin', methods=["GET"])
def get_auth_log():
    auth_log = fire_db.child('AUTH').get().val()
    return jsonify(auth_log)

@app.route('/api/obs/admin', methods=['GET'])
def get_obs_log():
    obs_log = fire_db.child('OBS').get().val()
    return jsonify(obs_log)

@app.route('/api/transactions/admin', methods=['GET', 'POST'])
def get_transactions():
    all_transactions = fire_db.child('transactions').get()
    return jsonify(all_transactions.val())

@app.route('/transaction_parse', methods=["GET", "POST"])
def parse_trans():
    all_transactions = requests.get('http://localhost:5000/api/transactions/admin').json()
    present_trans = []

    for user_value in all_transactions.values():
        try:
            for trans_value in user_value["bought"].values():
                present_trans.append(trans_value)
        except:
            continue
        
        try:
            for trans_value in user_value["sold"].values():
                present_trans.append(trans_value)
        except:
            continue

    return jsonify(sorted(present_trans, key=lambda i: i["created_at"], reverse=True))


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
    new_record = {
        'email': current_user.username, 
        'action': 'Added funds.', 
        'time': datetime.utcnow().strptime('%Y-%m-%dT%H:%M:%S.%f%z')
    }
    fire_db.child('OBS').child(current_user.username).push(new_record)

    req = request.get_json()


    insertFunds(str(current_user.username), returnAccount(), str(req["fundAmount"]))


    res = make_response(jsonify({"message": "OK"}), 200)

    return res



@app.route("/addAccount", methods=["POST"])
def addAccount():
    new_record = {
        'email': current_user.username, 
        'action': 'Added account.', 
        'time': datetime.utcnow().strptime('%Y-%m-%dT%H:%M:%S.%f%z')
    }
    fire_db.child('OBS').child(current_user.username).push(new_record)
    req = request.get_json()

    savedUser = str(current_user.username)
    savedAcc = str(req['newAccount'])
    print("saved user is " +savedUser )
    accCount = (accNum(savedUser))

    if (accCount <=2 and accCount > 0):
        signOutUsers()
        insert_user_table(savedUser, savedAcc, "0", "Y", "0", "0", "0", "0")
        res = make_response(jsonify({"message": "OK"}), 200)
    else:
        res = make_response(jsonify({"message": "Err - no more than 3 accounts"}), 200)
    return res


@app.route("/buy", methods=["POST"])
def buyShares():
    # Retrieve amount and its in JSON form
    new_record = {
        'email': current_user.username, 
        'action': 'Bought shares.', 
        'time': datetime.utcnow().strptime('%Y-%m-%dT%H:%M:%S.%f%z')
    }
    fire_db.child('OBS').child(current_user.username).push(new_record)

    req = request.get_json()
    token=generate_token(current_user.username)
    headers = {'token': token}
    
    buyAmount = (float) (req["buyAmount"]) #probably want float but dont know how your sql works
    symPass = str(req["Symbol"])
    data = {'amount': buyAmount}
    finalFund = (getPrevFunds(str(current_user.username), returnAccount()))
    cash = (float)(finalFund)

    # retrieve cash in account if symbol is AAPL and buyAmount *appl_shares < cash then store
    if (symPass == 'aapl'):
        aapl_price = requests.get('http://localhost:5001/aapl/share_price').json()["Price"]
        tot = buyAmount * aapl_price
        if (tot < cash):
            updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)
            aapl_buy = requests.get('http://localhost:5001/aapl/buy/', headers=headers, params=data)
            print(aapl_buy)

            res = make_response(jsonify({"message": "OK"}), 200)
            return res
        else:
            res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
            # print(tot)
            return res

    # if (symPass == 'msft'):
    #     msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]
    #     tot = buyAmount * msft_price
    #     if (tot < cash):
    #         updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)
    #         msft_buy = requests.get('http://localhost:5001/msft/buy/', headers=headers, params=data)
    #         print(msft_buy)

    #         res = make_response(jsonify({"message": "OK"}), 200)
    #         # print(tot)
    #         return res
    #     else:
    #         res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
    #         # print(tot)
    #         return res

    # if (symPass == 'fb'):
    #     fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]
    #     tot = buyAmount * fb_price
    #     if (tot < cash):
    #         updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)

    #         fb_buy = requests.get('http://localhost:5001/fb/buy/', headers=headers, params=data)
    #         print(fb_buy)
    #         res = make_response(jsonify({"message": "OK"}), 200)
    #         # print(tot)
    #         return res
    #     else:
    #         res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
    #         # print(tot)
    #         return res

    # if (symPass == 'googl'):
    #     goog_price = requests.get('http://localhost:5001/goog/share_price').json()["Price"]
    #     tot = buyAmount * goog_price
    #     if (tot < cash):
    #         updateShares(str(current_user.username), returnAccount(), symPass, True, buyAmount, tot)
    #         goog_buy = requests.get('http://localhost:5001/goog/buy/', headers=headers, params=data)
    #         print(goog_buy)
    #         res = make_response(jsonify({"message": "OK"}), 200)
    #         return res
    #     else:
    #         res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
    #         # print(tot)
    #         return res

    res = make_response(jsonify({"message": "OK"}), 200)

    return res


@app.route("/sell", methods=["POST"])
def sellShares():
    new_record = {
        'email': current_user.username, 
        'action': 'Sold shares.', 
        'time': datetime.utcnow().strptime('%Y-%m-%dT%H:%M:%S.%f%z')
    }
    fire_db.child('OBS').child(current_user.username).push(new_record)

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

    # if (symPass == 'msft'):
    #     # msft_price = requests.get('http://localhost:5001/msft/share_price').json()["Price"]

    #     tot = sellAmount * msft_price
    #     # add tot to cash val
    #     # subtract from appl shares
    #     # get current amount of appl shares and check if you are trying to sell less then the one you have
    #     if (sellAmount <= tot_shares):
    #         updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

    #         res = make_response(jsonify({"message": "OK"}), 200)
    #         return res
    #     else:
    #         res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
    #         # print(tot)
    #         return res

    # if (symPass == 'fb'):
    #     # fb_price = requests.get('http://localhost:5001/fb/share_price').json()["Price"]

    #     tot = sellAmount * fb_price
    #     # add tot to cash val
    #     # subtract from appl shares
    #     # get current amount of appl shares and check if you are trying to sell less then the one you have
    #     if (sellAmount <= tot_shares):
    #         updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

    #         res = make_response(jsonify({"message": "OK"}), 200)

    #         return res
    #     else:
    #         res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
    #         # print(tot)
    #         return res

    # if (symPass == 'googl'):
    #     # goog_price = requests.get('http://localhost:5001/goog/share_price').json()["Price"]

    #     tot = sellAmount * goog_price
    #     # add tot to cash val
    #     # subtract from appl shares
    #     # get current amount of appl shares and check if you are trying to sell less then the one you have
    #     if (sellAmount <= tot_shares):
    #         updateShares(str(current_user.username), returnAccount(), symPass, False, sellAmount, tot)

    #         res = make_response(jsonify({"message": "OK"}), 200)
    #         return res
    #     else:
    #         res = make_response(jsonify({"Error": "Not Enough Funds"}), 409)
    #         return res


    res = make_response(jsonify({"message": "OK"}), 200)
    return res

