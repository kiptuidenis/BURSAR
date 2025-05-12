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
try:
    with app.app_context():
        # Import models to ensure they're registered with SQLAlchemy
        from app.models import User, BudgetCategory, Transaction
        
        # Create all tables first
        db.create_all()
        print("Database tables created for Vercel environment")
        
        # Import and run the database initialization function
        try:
            from app.init_vercel_db import init_vercel_db
            # Initialize with sample data
            init_vercel_db()
        except Exception as e:
            print(f"Warning: Sample data initialization failed: {str(e)}")
            print("Continuing without sample data - application will still work")
except Exception as e:
    print(f"Error during database initialization: {e}")
    # This is critical, but we'll let the app continue and see if it works

# Handler class for Vercel - This MUST be named 'handler'
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # In serverless context, the database is recreated for each request
            # So we need to ensure the tables exist
            try:
                with app.app_context():
                    # Make sure tables exist
                    db.create_all()
            except Exception as db_err:
                print(f"Warning: Could not create tables for GET request: {db_err}")
                # Continue anyway and see if it works
            
            # Use Flask test client to handle the request
            with app.test_client() as test_client:
                # Map the path from the request to Flask
                response = test_client.get(self.path)
                
                self.send_response(response.status_code)
                for header, value in response.headers:
                    if header.lower() != 'content-length':  # Skip content-length as we set it
                        self.send_header(header, value)
                self.end_headers()
                
                self.wfile.write(response.data)
        except Exception as e:
            print(f"Error handling GET request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_message = f"<html><body><h1>Server Error</h1><p>{str(e)}</p></body></html>"
            self.wfile.write(error_message.encode('utf-8'))
        return

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # In serverless context, the database is recreated for each request
            # So we need to ensure the tables exist
            try:
                with app.app_context():
                    # Make sure tables exist
                    db.create_all()
            except Exception as db_err:
                print(f"Warning: Could not create tables for POST request: {db_err}")
                # Continue anyway and see if it works
            
            # Handle the POST request using Flask's test client
            with app.test_client() as test_client:
                content_type = self.headers.get('Content-Type', '')
                response = test_client.post(
                    self.path,
                    data=post_data,
                    content_type=content_type
                )
                
                self.send_response(response.status_code)
                for header, value in response.headers:
                    if header.lower() != 'content-length':  # Skip content-length as we set it
                        self.send_header(header, value)
                self.end_headers()
                
                self.wfile.write(response.data)
        except Exception as e:
            print(f"Error handling POST request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_message = f"<html><body><h1>Server Error</h1><p>{str(e)}</p></body></html>"
            self.wfile.write(error_message.encode('utf-8'))
        return