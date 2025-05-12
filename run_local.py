"""
Local development server script for the BURSAR application.
This script ensures proper environment setup before running the Flask app.
"""
import os
import sys
from app import create_app

# Set environment variables for local development
os.environ['FLASK_APP'] = 'wsgi.py'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    print("Starting BURSAR application in development mode...")
    print(f"Session type: {app.config.get('SESSION_TYPE')}")
    print(f"Session file directory: {app.config.get('SESSION_FILE_DIR')}")
    app.run(debug=True)
