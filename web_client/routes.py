from flask import render_template, url_for, flash, redirect, request,session,jsonify
from web_client import app, db, bcrypt
from web_client.forms import RegistrationForm, LoginForm
from web_client.models import User
import json
from flask_login import login_user, current_user, logout_user, login_required
import requests
from datetime import datetime, timedelta
import jwt
@app.route("/")
@app.route("/home")
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
          
           
            
            token = generate_token(user.username)
            return  redirect(url_for('home', token=json.dumps({'token':token.decode('UTF-8')})))
             
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
# Generates token
def generate_token( username, seconds=0, minutes=30, hours=0):
  
    exp_time =  datetime.utcnow() + \
        timedelta(seconds=seconds, minutes=minutes, hours=hours)

    payload = {'username': username,
               'iss': 'appl_api',
               'exp': exp_time
               }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token