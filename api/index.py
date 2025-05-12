from flask import Flask, Request, Response
from http.server import BaseHTTPRequestHandler
import sys
import os
import json

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app and db
from app import create_app, db

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

# Create database tables for SQLite in-memory database
with app.app_context():
    # Import models to ensure they're registered with SQLAlchemy
    from app.models import User, BudgetCategory, Transaction
    # Import the database initialization function
    from app.init_vercel_db import init_vercel_db
    
    # Initialize the database with tables and sample data
    init_vercel_db()
    print("Database initialized for Vercel environment")

# Handler class for Vercel - This MUST be named 'handler'
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # In serverless context, the database is recreated for each request
        # So we need to ensure the tables exist
        with app.app_context():
            # Make sure tables exist
            db.create_all()
        
        # Use Flask test client to handle the request
        with app.test_client() as test_client:
            # Map the path from the request to Flask
            response = test_client.get(self.path)
            self.wfile.write(response.data)
        return

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # In serverless context, the database is recreated for each request
        # So we need to ensure the tables exist
        with app.app_context():
            # Make sure tables exist
            db.create_all()
        
        # Handle the POST request using Flask's test client
        with app.test_client() as test_client:
            content_type = self.headers.get('Content-Type', '')
            response = test_client.post(
                self.path,
                data=post_data,
                content_type=content_type
            )
            self.wfile.write(response.data)
        return