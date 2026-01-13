# AWS Elastic Beanstalk entry point
# This file is required for Elastic Beanstalk deployment

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app

# Elastic Beanstalk expects the application to be named 'application'
application = app

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=False)