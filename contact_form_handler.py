##########################################################
"""

Purpose: 
This file handles the contact form submissions for your Flask web app. It processes the form data, saves it to the database, and sends a confirmation email to the user.

How it works:

read_credentials_from_file: Reads Google API credentials from a file.

write_credentials_to_file: Writes Google API credentials to a file.

credentials_to_json: Converts the credentials object to a JSON string.

send_email: Sends an email using the Gmail API, refreshing the token if expired.

handle_contact_form: Handles the submission of the contact form, processes the form data, saves it to the database, and sends a confirmation email to the user.

Where it’s used:
These functions are used in your Flask app to handle contact form submissions and send confirmation emails.
"""
#########################################################

#contact_form_handler.py
"""
This module handles the contact form submissions for the Flask web app. It processes the form data, saves it to the database, and sends a confirmation email to the user. 

also refreshes token if expired before trying to send mail

Dependencies:
- Flask: For rendering templates, handling requests, and flashing messages.
- contact_form: Contains the ContactForm class for form validation.
- models: Contains the Contact model for database interactions.
- database: Contains the db object for interacting with the database.
- google.oauth2.credentials: For handling Google API credentials.
- google.auth.transport.requests: For refreshing expired credentials.
- googleapiclient.discovery: For interacting with the Gmail API.
- utils: Contains utility functions such as get_all_keywords.

Constants:
- TOKEN_FILE: The file where Google API credentials are stored.
"""

#####################################################################
import os
import json
import time
import base64
from flask import render_template, flash, current_app, request, after_this_request
from contact_form import ContactForm
from models import Contact
from database import db
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from utils import get_all_keywords

##################################################################


##################################################################
# Function to read credentials from file

"""
    Reads Google API credentials from the specified file.

    Returns:
        Credentials: The credentials object if the file exists; None otherwise.
    """
def read_credentials_from_file():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token_file:
            data = json.load(token_file)
            return Credentials(**data)
    return None

##########################################################
# Function to write credentials to file
"""
    Writes Google API credentials to the specified file.

    Args:
        credentials (Credentials): The credentials object to write to the file.
    """
def write_credentials_to_file(credentials):
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(credentials_to_json(credentials))


#################################################################

"""
checks if token expired and then refreshes it using refresh token and then
    Sends an email using the Gmail API.

    Args:
        credentials (Credentials): The credentials object for authenticating with the Gmail API.
        msg (MIMEText): The email message to send.
    """
def send_email(credentials, msg):
    try:
        # Check if the token is expired and refresh it if necessary
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            write_credentials_to_file(credentials)  # Save refreshe


# Build the Gmail service and send the email
        service = build('gmail', 'v1', credentials=credentials)
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        message = {'raw': raw}
        send_message = service.users().messages().send(userId="me", body=message).execute()
        current_app.logger.info(f"Email sent to {msg['To']}.")
    except Exception as e:
        current_app.logger.error(f"Error sending email to {msg['To']}: {e}")

######################################################################

"""
    Handles the submission of the contact form.

    Processes the form data, saves it to the database, and sends a confirmation email to the user.

    Returns:
        str: The rendered HTML template for the contact form or success page.

    Flask-WTF handles CSRF token validation automatically
    """
def handle_contact_form():
    keywords = get_all_keywords()
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit(): ## This includes CSRF validation
            start_time = time.time()  # record start time
            try:
                # Log form data
      #          current_app.logger.info(f"Form Data: Name={form.name.data}, Email={form.email.data}, Message={form.message.data}")

                # Create a new Contact object
                new_contact = Contact(
                    name=form.name.data,
                    email=form.email.data,
                    message=form.message.data
                )

                # Add to the database
                db.session.add(new_contact)
                db.session.commit()

                # Log successful submission
                current_app.logger.info("Contact form successfully submitted and saved to the database.")

                # Render the success page
                response = render_template('contact_success.html', keywords=keywords)

                # Create a single email message for both the user and the admin and send mail
                msg = MIMEText(f"Hello {form.name.data},\n\nThank you for reaching out. I have received your message.\nWill get back to you soon.\n\nBest regards,\nAtul")
                msg['Subject'] = 'Tech With Atul - Contact Form Submission Received'
                msg['To'] = form.email.data
                msg['From'] = f"Tech With Atul <{current_app.config['MAIL_DEFAULT_SENDER']}>"
                msg['Bcc'] = current_app.config['MAIL_DEFAULT_SENDER']

                @after_this_request
                def send_emails(response):
                    credentials = read_credentials_from_file()
                    if credentials:
                        send_email(credentials, msg)
                    else:
                        current_app.logger.error("Error: No credentials found. Cannot send email.")
                    # Calculate and log the time taken to render the success page
                    elapsed_time = time.time() - start_time
                    current_app.logger.info(f"Time taken to render success page and send email: {elapsed_time:.2f} seconds")
                    return response

                return response

            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Database error: {e}")
                flash(f"An error occurred while submitting the form: {str(e)}", "danger")
                return render_template('contact.html', form=form, keywords=keywords)

        else:
            current_app.logger.info(f"Form Errors: {form.errors}")
            flash("Please correct the errors and try again.", "danger")

    return render_template('contact.html', form=form, keywords=keywords)

