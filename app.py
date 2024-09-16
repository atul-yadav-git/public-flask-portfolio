###########################################################
#app.py

'''
Purpose:
This file sets up and runs your Flask web portfolio app.


How it works:

Environment Variables: Loads environment variables from a .env file.

Flask App Initialization: Initializes the Flask app and configures various settings.

Logging: Sets up logging using a custom logging configuration.

Database: Configures and initializes the SQLite database using SQLAlchemy and Flask-Migrate.

Admin Interface: Sets up the Flask-Admin interface for managing the app.

OAuth 2.0 Flow: Configures OAuth 2.0 for Gmail API integration.

Error Handlers: Defines custom error handlers for 404 and 500 errors.

Flask-Login: Initializes Flask-Login for user authentication.

Routes: Defines various routes for the web app, including home, contact, login, job experience, blogs, projects, and resume pages.

Where it’s used:
This file is the main entry point for your Flask web portfolio app and is used to configure and run the app.
'''

#########################################################################

import os
from flask import Flask, render_template, request, flash, send_from_directory, redirect, url_for, session
from flask_login import LoginManager, login_user
from dotenv import load_dotenv # for environment variables to load in flask app
#from werkzeug.security import check_password_hash  # Import the function to check password hash
from datetime import timedelta
from flask_migrate import Migrate # to handle schema changes in code
from flask_mail import Mail # for extending flask email functionaility
from google_auth_oauthlib.flow import InstalledAppFlow
import json
from flask_wtf import CSRFProtect
########################################################

#Importing Custom modules for differnet functionalities

from admin import setup_admin #this is my admin setup code in admin.py for admin panel setup
from models import  User, Post, Project # Import the Post and Project models ; database models
from database import db #import the database instance from database.py
from logging_config import setup_logging #calling logging modulein main app code; logging setup
from contact_form_handler import handle_contact_form, write_credentials_to_file# Import the contact form handling function
from admin_setup import add_admin_user  # Import the function to add the admin user; admin user setup
from search_logic import search_posts, search_projects #my serach query functionality separate file; search logic for post projects
from utils import get_all_keywords #utility function to fetch keywords
from admin_login import admin_login_form, LoginForm #for admin interface login

##################################################


# Load environment variables from .env file
load_dotenv()



#Initialize flask app
app = Flask(__name__)

#configure application settings
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-default-secret-key') #This key is used by Flask-WTF to protect against CSRF attacks.

csrf = CSRFProtect(app) #flask-wtf form automaticaaly generates csrf token using secret key and handles validation also

# Initialize logging
setup_logging(app)#calling log function before app runs

# Set up the SQLite database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'career_page.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db ; so that flask app and sqlalchemy are associated with each other
db.init_app(app)


# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)


# Set up admin interface
setup_admin(app)  # Initialize the admin interface


#create database before initializing application
# Ensure the database is created when the app starts and add admin user if doesnt exists
with app.app_context():
    db.create_all()
    add_admin_user(app)  # Add admin user if not exists; call admin setup function

#Initialize flask-mail
mail = Mail(app)

# Set up the OAuth 2.0 flow for gmail api
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'creedentials.json')

#OAuth authorization route
@app.route('/authorize')
def authorize():
    """Initiate the OAuth 2.0 authorization process."""
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = url_for('oauthcallback', _external=True)
    authorization_url, state = flow.authorization_url
    (
        prompt='consent',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

#OAuth callback route
@app.route('/oauthcallback')
def oauthcallback():
    """Handle the OAuth 2.0 callback and obtain credentials."""
    state = session['state']
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES, state=state)
    flow.redirect_uri = url_for('oauthcallback', _external=True)
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials


    # Store OAuth 2.0 credentials for future use
    write_credentials_to_file(credentials)
    
    return redirect(url_for('contact'))


# Custom error handler for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # Render a custom 404 page

# Custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f'Server Error: {e}')
    return render_template('500.html'), 500


# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view custom url for security

@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database."""
    return User.query.get(int(user_id))

#actual web application code
@app.route('/')
def home():

   # app.logger.info('Home page accessed')
    # Fetch recent blogs and projects from the database
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    recent_projects = Project.query.order_by(Project.date_created.desc()).limit(3).all()
     # Fetch keywords for the dropdown
    keywords = get_all_keywords()

    return render_template('index.html', recent_posts=recent_posts, recent_projects=recent_projects, keywords=keywords)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page and handle form submissions."""
    # Fetch keywords for the dropdown
    keywords = get_all_keywords()

    return handle_contact_form()  # Use the separated contact form handling logic ; passing mail object to the route handler


#admin login page route
@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Render the login page and handle user authentication."""
    
    form = LoginForm()
    return admin_login_form(form)#use login logic from admin_login module


# Static experience page route
@app.route('/job_experience')
def job_experience():

    # Fetch keywords for the dropdown
    keywords = get_all_keywords()
    return render_template('experience.html', keywords=keywords)

# Blog page route
@app.route('/blogs')
def blogs():
    """Render the blogs page with paginated posts."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    keywords = get_all_keywords()
    return render_template('blogs.html', keywords=keywords)

# Project page route
@app.route('/projects')
def projects():
    """Render the projects page with paginated projects."""
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.date_created.desc()).paginate(page=page, per_page=4) #4 projects per page, latest date
    keywords = get_all_keywords()
    return render_template('projects.html',  keywords=keywords)

# Resume page route
@app.route('/resume')
def resume():
    keywords = get_all_keywords()
    return render_template('resume.html', keywords=keywords)



# Search functionality
@app.route('/search')
def search():
    """Perform search on posts and projects."""
    valid_keywords = get_all_keywords()
    query = request.args.get('query','').strip()
    posts_page = request.args.get('posts_page', 1, type=int)
    projects_page = request.args.get('projects_page', 1, type=int)
   # keywords = [query]

    #search for post and projects
    posts_query = search_posts([query])
    posts = posts_query.paginate(page=posts_page, per_page=3)

    projects_query = search_projects([query])
    projects = projects_query.paginate(page=projects_page, per_page=3)

    return render_template('search_results.html')

############################3######################################
#if i run flask app in local server without gunicorn and nginx then this is used
###########################################################

if __name__ == '__main__': #this checks if app is imported as module or locally
    app.run(debug=False, host='0.0.0.0', port=80) #start flask server for locall testing

######################################################################
