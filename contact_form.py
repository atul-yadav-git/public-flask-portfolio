# contact_form.py
# This file defines the contact form used in the Flask web portfolio app.
# It uses Flask-WTF to create a form with fields for name, email, and message,
# along with validation to ensure the fields are filled out correctly.

########################################################

# Import necessary modules from Flask-WTF and WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

#########################################################

# Define the ContactForm class which is a form for handling contact requests

"""
    ContactForm class defines the form used for handling contact submissions on the website.
    
    This form is created using Flask-WTF and WTForms. It includes fields for the user's name, email address, 
    and message, along with a submit button. Each field is validated to ensure required data is provided and, 
    in the case of the email field, that the data entered is a valid email address.
    
    Fields:
        name (StringField): The name of the person contacting.
        email (StringField): The email address of the person contacting, must be in a valid email format.
        message (TextAreaField): The message content that the person is sending.
        submit (SubmitField): The button used to submit the form.
    """
class ContactForm(FlaskForm):

    # Field for the user's name, required field
    name = StringField('Name', validators=[DataRequired()])
   
    # Field for the user's email, required field and must be a valid email format
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Field for the user's message, required field
    message = TextAreaField('Message', validators=[DataRequired()])
    
    # Submit button for the form
    submit = SubmitField('Submit')

