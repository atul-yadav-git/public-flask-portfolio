"""
admin_login.py

This module handles admin login functionality for the Flask web application.

Components:
- `LoginForm`: Defines a form with username and password fields for login.
- `admin_login_form(form)`: Processes the login form, validates credentials, and manages user sessions.

Usage:
1. **Form Handling**: `admin_login_form` initializes and validates a `LoginForm`. 
2. **Authentication**: Retrieves user data from the `User` model and checks the hashed password.
3. **Session Management**: On successful login, `login_user` is called to start a user session. Redirects to the admin interface or back to the login page on failure.

Dependencies:
- `FlaskForm`, `StringField`, `PasswordField`, `SubmitField` from `wtforms`.
- `render_template`, `flash`, `redirect`, `url_for` from `flask`.
- `User` model and `check_password_hash` from `werkzeug.security`.
- `login_user` from `flask_login`.

Note: Ensure that the `User` model and necessary routes are correctly set up in your Flask application.
"""




#######################################################

from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, flash, current_app, request, after_this_request, redirect, url_for, session
from models import  User
from werkzeug.security import check_password_hash  # Import the function to check password hash
from flask_login import  login_user

################################################################
# Define a simple login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



def admin_login_form(form):
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admiin.index'))  # Redirect to the admin interface
        flash('Invalid username or password')
        return redirect(url_for('login'))

