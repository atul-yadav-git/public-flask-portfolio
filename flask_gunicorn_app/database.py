# database.py
# This file sets up the SQLAlchemy instance for the Flask web portfolio app.
# SQLAlchemy is used as the ORM (Object-Relational Mapping) tool to interact with the database.; # SQLAlchemy is used for managing database operations and interactions.
##################################################################

"""
Purpose:
- This file initializes the SQLAlchemy instance, which will be used throughout the Flask app to interact with the database.

How it works:
- The `SQLAlchemy` class is imported from the `flask_sqlalchemy` module.
- An instance of `SQLAlchemy` is created and assigned to the variable `db`.
- This instance (`db`) will be used to define models and perform database operations.

Where it's used:
- The `db` instance is imported and used in other parts of the Flask app, such as in the `models.py` file to define database models and in the main application file to initialize the database with the Flask app.
"""

############################################################3



from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #create the sqlalchemy instance

