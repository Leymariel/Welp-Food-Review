from app import app
from flask import Flask, request, redirect, url_for, session, render_template
from .models.user import User
from .models.business import Business

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        info = User.getUserByEmail(email)
        if info:
            user = User(info[1], info[2], info[3], info[4])
            print(info)
            if user and user.checkPassword(password):
        
                return redirect(url_for('main_page'))  # Redirect to the main page after login
            else:
                # If login failed
                return render_template('index.html', error="Invalid credentials")
                
    return render_template('index.html')


from flask import session

@app.route('/business-login', methods=['GET', 'POST'])
def business_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        info = Business.getBusinessByEmail(email)
        if info:
            business = Business(info[0], info[1], info[2], info[3], info[4], info[6], info[8])
            if business and business.checkPassword(password):
                session['business_id'] = info[0]  # Set business ID in session
                return redirect(url_for('business_portal'))
            else:
                return render_template('business-login.html', error="Invalid credentials")

    return render_template('business-login.html')


@app.route('/business-portal', methods=['GET', 'POST'])
def business_portal():
    # Check if a business is logged in and get their ID
    business_id = session.get('business_id')
    if not business_id:
        return redirect(url_for('business_login'))  # or any appropriate login route

    if request.method == 'POST':
        # Handle profile picture upload
        file = request.files['profile_picture']
        if file:
            blob_data = file.read()
            business = Business.getBusinessByID(business_id)
            business.setPhoto(blob_data)
            
            flash("Profile picture updated successfully!")
            return redirect(url_for('business_portal'))

    # Fetch the current business details for display

    business_info = Business.getBusinessByID(business_id)
    
    # Pass the business information to the template
    return render_template('business-portal.html', business=business_info)

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

@app.route('/create-user', methods=['GET', 'POST'])
def create_account():
    print(request.method)
    if request.method == 'POST':

        # Return the account creation page
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        passwordConf = request.form['passwordConf']

        if password != passwordConf:
            return render_template('create-user.html', error = "Passwords do not match")

        user = User.getUserByEmail(email)
        if user:
            return render_template('create-user.html', error ="Email already in use")
        else:
            newUser = User(username, password, email)
            newUser.createNew()
    # Return the business creation page
    return render_template('create-user.html')

@app.route('/main-page', methods=['GET', 'POST'])
def main_page():
    # Return the account creation page
    businesses = Business.getAll()
    print(businesses)
    return render_template('main-page.html', restaurants=businesses)


@app.route('/business/<int:id>')
def business_page(id):
    # Fetch the business details from the database using email
    business = Business.getBusinessByEmail(id) 
    return render_template('business_page.html', business=business)


@app.route('/image/<int:business_id>')
def serve_image(business_id):
    
    business_info = Business.getBusinessByID(business_id)
    business = Business(*business_info)
    image_data = business.getPhoto()

    if image_data and image_data[0]:
        return Response(image_data[0], mimetype='image/jpeg')  # Adjust MIME type if necessary
    else:
        return "No image found", 404

@app.route('/search-results')
def search_results():
    query = request.args.get('query')

    # Perform search logic using your Business class
    results = Business.search(query)

    # Render the search results template with the search results
    return render_template('search_results.html', results=results)