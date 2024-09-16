# Gunicorn configuration file for Flask web portfolio app
#########################################################
#Purpose: This file configures Gunicorn, a WSGI HTTP server for serving Flask applications. It defines settings such as server socket, worker processes, timeouts, and logging.
######################################################


###########################################################
# Server Socket Configuration
# The 'bind' option specifies the socket or address to which Gunicorn should bind.
# In this configuration, we are using a Unix socket for communication between Gunicorn and Nginx.
# This is preferred for performance and security reasons compared to using a TCP socket.
# Uncomment the line below to use a TCP socket instead:
bind = "0.0.0.0:8000"
#bind = "unix:/var/run/gunicorn/gunicorn.sock"  # Unix socket location for communication with Nginx

##################################################################
# Worker Processes
# The 'workers' option defines the number of worker processes Gunicorn will use to handle requests.
# Each worker process can handle one request at a time. Having multiple workers allows handling
# multiple requests concurrently. The number of workers should generally be set based on the
# number of CPU cores available. A common guideline is to use (2 x number of CPU cores) + 1.
##workers = 3  # Number of concurrent worker processes

# Uncomment the lines below to use the 'gthread' worker class, which allows for handling
# concurrent requests using threads. This can be useful for I/O-bound applications.
# worker_class = 'gthread'  # Use 'gthread' worker class for handling concurrent threads
# threads = 4  # Number of threads per worker process; adjust as needed based on concurrency requirements

##########################################################
# Worker Timeout
# The 'timeout' option defines the maximum amount of time (in seconds) that a worker can take
# to handle a request before being killed and restarted. This helps in ensuring that hung
# or stuck requests are automatically cleaned up.
##timeout = 120  # Timeout for worker processes (in seconds)

###########################################################
# Logging Configuration
# The 'loglevel' option specifies the granularity of log messages. Common values are 'debug',
# 'info', 'warning', 'error', and 'critical'. In this configuration, we use 'info' level logging
# which provides a balance of log detail and verbosity.
loglevel = 'info'

# 'accesslog' specifies the file path where access logs will be written. These logs contain
# information about incoming requests to the server.
accesslog = '/var/log/gunicorn/access.log'

# 'errorlog' specifies the file path where error logs will be written. These logs capture
# error messages and stack traces from the application.
errorlog = '/var/log/gunicorn/error.log'

###################################################
# General Information
# - `bind`: Defines the address or socket Gunicorn uses for communication with clients (Nginx).
# - `workers`: Determines the number of worker processes handling requests. Adjust based on CPU cores.
# - `worker_class` and `threads`: Options for specifying worker type and threading; useful for I/O-bound tasks.
# - `timeout`: Sets the maximum request handling time before a worker is restarted.
# - `loglevel`, `accesslog`, and `errorlog`: Configure logging verbosity and log file paths.
# 
# Ensure that the paths for Unix sockets and log files are correctly configured and accessible by
# Gunicorn and Nginx. Adjust the number of workers and threads based on your application's needs
# and server resources.

