#All system-level packages and installations

#!/bin/bash

# Update system packages
sudo dnf upgrade -y

# Install required system packages
sudo dnf install python3 sqlite -y   # Ensure Python and SQLite are installed
sudo dnf install nginx -y            # Install Nginx
sudo dnf install gunicorn -y         # Install Gunicorn

# Install Certbot for SSL setup with Let's Encrypt
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y
sudo dnf install certbot -y
sudo dnf install python3-certbot-nginx -y  # Certbot integration with Nginx

# Install and run Nikto for security scans
sudo dnf install perl git -y
git clone https://github.com/sullo/nikto
cd nikto/program
./nikto.pl -h http://techwithatul.com  # Basic scan

# Inform user that the setup is complete
echo "System-level dependencies installed. Now run 'pip install -r requirements.txt' to install Python dependencies."
