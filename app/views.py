from app import app
from flask import Flask, request, redirect, url_for, session, render_template
from .models.user import User

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        info = User.getUserByUsername(username)
        if info:
            user = User(info[0], info[1], info[2], info[3], info[4])
            if user and user.checkPassword(password):
        
                return render_template('main-page.html') # Redirect to the main page after login
            else:
                # If login failed
                return render_template('index.html', error="Invalid credentials")
        
        print(user)
        
    return render_template('index.html')


@app.route('/business-login')
def business_login():
    # Return the business login page
    return render_template('business-login.html')

@app.route('/create-business')
def create_business():
    # Return the business login page
    return render_template('create-business.html')

@app.route('/create-account')
def create_account():
    # Return the account creation page
    return render_template('create_account.html')

@app.route('/main-page')
def main_page():
    # Return the account creation page
    return render_template('main-page.html')