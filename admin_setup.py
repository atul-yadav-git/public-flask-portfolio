#logic to add admin user from configured environmnet variable during app initialization if it doesnt already exits in db


'''
Explanation:

Purpose: This script sets up an administrative user for your Flask application, ensuring there is at least one admin user in the system. It uses environment variables to obtain the credentials and handles cases where the admin user might already exist.

How it Works:
Retrieves ADMIN_USERNAME and ADMIN_PASSWORD from environment variables.
Checks if an admin user with the specified username already exists in the database.
If not, it creates a new user with the provided credentials, hashes the password, and saves it to the database.
Handles errors, including database integrity issues and other exceptions, and performs a rollback if necessary.

Where it’s Used: This file is used during the application initialization process to ensure that an admin user is present before the application is fully operational. It is typically invoked as part of the setup or deployment process.

Raises:
        ValueError: If environment variables for ADMIN_USERNAME or ADMIN_PASSWORD are not set.

'''

###########################################################

import os
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from models import db, User

def add_admin_user(app):

    # Retrieve the admin username and password from environment variables
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')

    # Ensure both environment variables are set
    if not admin_username or not admin_password:
        app.logger.error("ADMIN_USERNAME and ADMIN_PASSWORD must be set in the environment variables.")
        raise ValueError("ADMIN_USERNAME and ADMIN_PASSWORD must be set in the environment variables.")

    # Debugging print to ensure environment variables are set correctly
    #print(f"Admin Username: {admin_username}")
    app.logger.info(f"Admin Username: {admin_username}")
    
    try:

        # Check if an admin user with the given username already exists
        existing_admin = User.query.filter_by(username=admin_username).first()

        if not existing_admin:
            # Hash the provided password
            hashed_password = generate_password_hash(admin_password)
            # Create a new admin user with the hashed password in database
            new_admin = User(username=admin_username, password=hashed_password, is_admin=True)
            
            # Add the new admin user to the session and commit the transaction
            db.session.add(new_admin)
            db.session.commit()

            # Confirm that the admin user was added successfully
            app.logger.info(f"Admin user '{admin_username}' added to the database.")
            #print(f"Admin user '{admin_username}' added to the database.")
        else:

            # Inform that the admin user already exists
            app.logger.info(f"Admin user '{admin_username}' already exists.")
            #print(f"Admin user '{admin_username}' already exists.")

    except IntegrityError as e:
        # Rollback in case of integrity error to avoid session problems (eg. duplicate entry)
        db.session.rollback()
        #print(f"IntegrityError: {e}")
        app.logger.error(f"IntegrityError: {e}")
    except Exception as e:
        # Catch any other exceptions and print the error message
        #print(f"An error occurred: {e}")
        app.logger.error(f"An error occurred: {e}")

