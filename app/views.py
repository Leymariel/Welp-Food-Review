from app import app
from flask import Flask, request, redirect, url_for, session, render_template, flash, jsonify
from base64 import b64encode
from .models.user import User
from .models.business import Business
from .models.review import Review
from .models.db_operations import db_operations

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        info = User.getUserByEmail(email)
        if info:
            user = User(*info)
            
            session['user_id'] = info[0]
            print(info)
            if user and user.checkPassword(password):
        
                return redirect(url_for('main_page'))  # Redirect to the main page after login
            else:
                # If login failed
                return render_template('index.html', error="Invalid credentials")
                
    return render_template('index.html')


@app.route('/business-login', methods=['GET', 'POST'])
def business_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        info = Business.getBusinessByEmail(email)
        print(info)
        if info:
            business = Business(*info)
            if business and business.checkPassword(password):
                session['business_id'] = info[0]  # Set business ID in session
                return redirect(url_for('business_portal'))
            else:
                return render_template('business-login.html', error="Invalid credentials")

    return render_template('business-login.html')


@app.route('/business-portal', methods=['GET', 'POST'])
def business_portal():
    db_ops = db_operations()
    categories = db_ops.get_all('Categories')

    business_id = session.get('business_id')
    if not business_id:
        return redirect(url_for('business_login'))

    business_info = Business.getBusinessByID(business_id)
    if not business_info:
        flash("Business information not found", "error")
        return redirect(url_for('business_login'))

    business = Business(*business_info)

    reviews = Business.getReviews(business_id)
    reviews_with_usernames = [(review + (User.getUserByID(review[2])[1],)) for review in reviews]
    
    photo_binary = business.getPhoto()
    photo_base64 = b64encode(photo_binary).decode("utf-8") if photo_binary else None

    return render_template('business-portal.html', BusinessPhoto=photo_base64, business_info=business_info, reviews=reviews_with_usernames, categories=categories)


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
            newBusiness = Business.createNew(businessName, address, phone, password, email, description)
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
            newUser = User.createNew(username, password, email)
    # Return the business creation page
    return render_template('create-user.html')

@app.route('/main-page', methods=['GET', 'POST'])
def main_page():
    db_ops = db_operations()
    businesses = Business.getAll()
    temp_businesses = []
    for business in businesses:
        temp_business = business
        if isinstance(business, tuple):
            category_id = business[11]
            print(category_id is not None)
            if category_id is not None:
                print("hello word")
                # Fetch the category name from the Categories table
                category_name = db_ops.get_category_name(category_id)
                print(category_name)
                # Add the category name to the business dictionary
                temp_business += (category_name,)
            else:
                temp_business += ("",)
            temp_businesses.append(temp_business)
    print(temp_businesses)

                
    return render_template('main-page.html', Businesses=temp_businesses)

@app.route('/business/<int:id>')
def business_page(id):
    business = Business.getBusinessByID(id)  # Fetch the business details

    # Fetch reviews for the business
    reviews = Business.getReviews(id)
  
    # Add usernames to the reviews
    reviews_with_usernames = []
    for review in reviews:
        user_id = review[2]  # Assuming the user ID is at index 2
        username = User.getUserByID(user_id)[1]
        reviews_with_usernames.append(review + (username,))  # Append username to the review tuple

    return render_template('business_page.html', business=business, reviews=reviews_with_usernames)


@app.route('/search-results')
def search_results():
    query = request.args.get('query')

    # Perform search logic using your Business class
    results = Business.search(query)

    # Render the search results template with the search results
    return render_template('search_results.html', results=results)


@app.route('/submit-review/<int:business_id>', methods=['POST'])
def submit_review(business_id):
    user_id = session['user_id']
    print("userid:", user_id)
    if not user_id:
        flash("You must be logged in to submit a review.", "error")
        return redirect(url_for('business_page', id=business_id))

    rating = request.form['rating']
    review_text = request.form['reviewText']
    newReview = Review(business_id, user_id, rating, review_text)
    newReview.addReview()
    db_ops = db_operations()

    query = f"SELECT AVG(Rating) FROM Reviews WHERE BusinessID = {business_id}"
    avg = db_ops.get_agg(query)
    b_info = Business.getBusinessByID(business_id)

    business = Business(*b_info) 
    
    business.updateRating(avg[0])
    # Add logic to save the review to your database here
    
    flash("Review submitted successfully!", "success")
    return redirect(url_for('business_page', id=business_id))



@app.route('/update-business-info', methods=['POST'])
def update_business_info():
    business_id = session.get('business_id')

    if not business_id:
        flash("You need to be logged in to update business information.", "error")
        return redirect(url_for('business_login'))

    # Extract form data
    business_name = request.form.get('business_name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')
    description = request.form.get('description')
    
    category_id = request.form.get('categoryID')


    file = request.files.get('profile_picture')
    if file:
        file_id = upload_to_drive(file)
        file_url = f"https://drive.google.com/uc?id={file_id}"
        print(file_url)

        flash("Profile picture updated successfully!")
        return redirect(url_for('business_portal'))

    business_id = session.get('business_id')
    business_info = Business.getBusinessByID(business_id)
    business = Business(*business_info)
    business.updateDetails(business_name, address, phone, email, description, category_id)

    # Save changes to the database (assuming your Business class has a method to do this)
    business.updateDetails(business_name, address, phone, email, description, category_id)

    flash("Business information updated successfully!", "success")
    return redirect(url_for('business_portal'))


@app.route('/logout', methods=['POST'])
def logout():
    # Remove 'user_id' from session
    session.pop('user_id', None)
    return redirect(url_for('index'))

SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Function to get Google Drive service
def get_google_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        'app/api/credentials.json', scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)
    return service

# Flask route to handle file upload
@app.route('/upload-to-drive', methods=['POST'])
def upload_to_drive(file):
    
    if file.filename == '':
        return 'No selected file'
    if file:
        service = get_google_drive_service()
        file_metadata = {'name': file.filename}
        media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return f'File ID: {file.get("id")}'
    
@app.route('/get-categories', methods=['GET'])
def get_categories():
    # Fetch categories from the database
    categories = db_operations.get_categories()
    return jsonify(categories)

@app.route('/submit-business', methods=['POST'])
def submit_business():
    # Create an instance of the db_operations class
    db_ops = db_operations()

    selected_category_name = request.form['categoryName']
    category_id = db_ops.get_category_id(selected_category_name)

    # Check if category_id is not None before further processing
    if category_id is not None:
        # Code to update the businesses table with the category_id
        # (You can use db_ops.send_query or any other method you have in your db_operations class)

        flash("Business submitted successfully!", "success")
    else:
        flash("Invalid category selected", "error")

    # Don't forget to close the connection when done
    db_ops.destructor()

    return redirect(url_for('main_page'))
