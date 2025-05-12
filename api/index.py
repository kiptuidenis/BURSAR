from flask import Flask, jsonify
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

# Simple HTTP handler function - this is critical for Vercel serverless
def handler(event, context):
    """
    Serverless function handler for Vercel
    
    This is a simple handler that returns the Flask WSGI app
    """
    try:
        # For direct invocation and health checks
        if event.get('path') == '/api/health':
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "ok",
                    "message": "API is running"
                }),
                "headers": {
                    "Content-Type": "application/json"
                }
            }
            
        # Normally just return the Flask app
        return app
        
    except Exception as e:
        # Return error information to help with debugging
        error_msg = str(e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": error_msg,
                "message": "An error occurred in the handler function"
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
            "body": response.data.decode('utf-8')
        }