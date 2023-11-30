from app import app
from flask import Flask, request, redirect, url_for, session, render_template
from .models.user import User
from .models.business import Business

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        username = request.form['email']
        password = request.form['password']

        info = User.getUserByEmail(username)
        if info:
            user = User(info[0], info[1], info[2], info[3], info[4])
            if user and user.checkPassword(password):
        
                return render_template('main-page.html') # Redirect to the main page after login
            else:
                # If login failed
                return render_template('index.html', error="Invalid credentials")
                
    return render_template('index.html')


@app.route('/business-login', methods=['GET', 'POST'])
def business_login():
    # Return the business login page
    return render_template('business-login.html')

@app.route('/create-business', methods=['GET', 'POST'])
def create_business():
    print(request.method)
    if request.method == 'POST':
        
        businessName = request.form['business_name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        description = request.form['description']
        password = request.form['password']
        passwordConf = request.form['passwordConf']

        if password != passwordConf:
            return render_template('create-business.html', error="Passwords do not match")

        business = Business.getBusinessByEmail(email)
        if business:
            return render_template('create-business.html', error="Email already in use")
        else:
            newBusiness = Business(businessName, address, phone, password, email, description)
            newBusiness.createNew()
    # Return the business creation page
    return render_template('create-business.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    # Return the account creation page
    return render_template('create_account.html')

@app.route('/main-page', methods=['GET', 'POST'])
def main_page():
    # Return the account creation page
    return render_template('main-page.html')