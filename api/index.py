from flask import Flask
import sys
import os

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

# Create Flask application with Vercel config
app = create_app(VercelConfig)

# Vercel serverless function handler
from flask import Response
import json

def handler(request):
    """
    Serverless function handler for Vercel
    
    This function adapts the Flask app to work with Vercel's serverless environment
    """
    # Get path and method from request
    path = request.get('path', '/')
    http_method = request.get('method', 'GET')
    
    # Prepare headers and body for test_client
    headers = request.get('headers', {})
    body = request.get('body', '') 
    
    # Handle the request with Flask's test client
    with app.test_client() as test_client:
        # Invoke the Flask application
        response = test_client.open(
            path, 
            method=http_method,
            headers=headers,
            data=body
        )
        
        # Prepare the response for Vercel
        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.data.decode('utf-8')
        }