from flask import Flask
import sys
import os
import json

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import create_app

# Create app config for Vercel serverless
class VercelConfig:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vercel-deployment-key'
    
    # SQLite setup for Vercel (using in-memory for serverless)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask settings
    DEBUG = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for serverless environment
    
    # Disable file system operations that cause errors in serverless environment
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False}
    }

# Create Flask application with Vercel config
app = create_app(VercelConfig)

# This is the handler that Vercel serverless functions use - MUST be named 'handler'
def handler(request, context):
    """
    Simple handler function for Vercel serverless
    
    This just returns the Flask app as an ASGI application
    """
    # Just return the Flask app - Vercel will handle the rest
    return app