from flask import Flask
import os

# Create Flask app
app = Flask(__name__)

# Import routes after app is created to avoid circular imports
from app.routes import *

# Vercel requires the app variable to be exposed
app.debug = os.environ.get('DEBUG', 'False').lower() == 'true'

# Handler for serverless function
def handler(request):
    """Handle requests in a serverless context."""
    return app(request)

# Only run the application directly when in development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
