# logging_config.py
# This module configures logging for the Flask web portfolio app.
# It sets up a TimedRotatingFileHandler to manage log files,
# rotating them daily and keeping logs for a maximum of 10 days.

##############################################################

'''
Purpose: This file sets up the logging configuration for your Flask web portfolio app.

How it works:

setup_logging: This function configures a timed rotating file handler to log error messages to a file with a date timestamp if the app is not in debug mode.

TimedRotatingFileHandler: Creates a file handler that rotates the log file at midnight each day and keeps up to 10 backup log files.

Log File Naming: The log files will be named error.log, error.log.1, error.log.2, etc., with the most recent log file being error.log.

Logging Level: Sets the logging level to DEBUG to capture detailed log messages.

Formatter: Formats the log messages to include the timestamp, log level, and message.

Where it’s used: This function is called during the initialization of your Flask app to set up logging.
'''

###############################################################


import logging
from logging.handlers import TimedRotatingFileHandler

#########################################################
"""
    Configures logging for the Flask application.

    This function sets up a TimedRotatingFileHandler that creates a new log file
    every day at midnight and keeps a maximum of 10 backup files. The logs are
    stored in files with a timestamp indicating the date. It ensures that only
    recent log files are retained, and older files are automatically deleted.

    Args:
        app (Flask): The Flask application instance to configure logging for.
    
    Functionality:
        - If the application is not in debug mode, it sets up a file handler
          for logging.
        - The log files are rotated at midnight, and old log files are kept for
          up to 10 days.
        - The logging level is set to DEBUG, which records all levels of logs
          including DEBUG, INFO, WARNING, ERROR, and CRITICAL.
        - Logs are formatted to include timestamps, log levels, and the log
          messages.

    Exceptions:
        - If logging setup fails, an error message is logged.
"""


def setup_logging(app):
    try:
        if not app.debug:
            # Create a TimedRotatingFileHandler for logging.
            file_handler = TimedRotatingFileHandler(
                    'error.log', #base log file name
                    when='midnight',  # Rotate at midnight
                    interval=1,  # Interval in days
                    backupCount=10 #keep logs for 10 days
                    )
            file_handler.setLevel(logging.DEBUG)# Set logging level to DEBUG
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            

            # Add the file handler to the app's logger
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.DEBUG) #INFO
            #print("Logging setup completed successfully.")
            app.logger.info("Logging setup completed successfully.")
    except Exception as e:
        # Log an error message if logging setup fails
        #print(f"Logging setup failed: {e}")
        app.logger.error(f"Logging setup failed: {e}")

