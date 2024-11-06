# wsgi.py
# This file serves as the entry point for the WSGI server (Gunicorn) to run the Flask application.
# It imports the Flask application instance from the app module and runs it.
###########################################################

from app import app # Import the Flask application instance


###############################################################

# The following block is commented out because it is used for local development only.
# When using Gunicorn and Nginx in a production environment, this block is not needed.
# Gunicorn will use the 'app' instance to serve the Flask application.

#if __name__ == "__main__":  # Check if the script is run directly (not imported as a module
 #   app.run()  # Run the Flask application locally for development without gunicorn and nginx


# When executed directly, the Flask application will be started with the built-in development server.

