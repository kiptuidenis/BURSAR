from flask import Flask, Request, Response
from http.server import BaseHTTPRequestHandler
import sys
import os
import json
import traceback

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
    TESTING = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for serverless environment
    
    # Session settings for serverless
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_session'  # Use /tmp directory in Vercel
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30  # 30 days in seconds
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Remember me cookie settings
    REMEMBER_COOKIE_DURATION = 3600 * 24 * 30  # 30 days in seconds
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    
    # Disable file system operations that cause errors in serverless environment
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False}
    }
    
    # Vercel flag
    VERCEL = True

# Create Flask application with Vercel config
app = create_app(VercelConfig)

# Initialize database on startup
try:
    with app.app_context():
        # Import models to ensure they're registered with SQLAlchemy
        from app.models import User, BudgetCategory, Transaction
        
        # Create all tables
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
    traceback.print_exc()

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
            
            # Extract cookies from request headers
            cookies = {}
            if 'Cookie' in self.headers:
                cookie_header = self.headers['Cookie']
                cookie_parts = cookie_header.split('; ')
                for part in cookie_parts:
                    if '=' in part:
                        name, value = part.split('=', 1)
                        cookies[name] = value
            
            # Use Flask test client to handle the request
            with app.test_client() as test_client:
                # Set cookies in the test client
                for name, value in cookies.items():
                    test_client.set_cookie('', name, value)
                
                # Map the path from the request to Flask
                response = test_client.get(
                    self.path, 
                    headers={k: v for k, v in self.headers.items() 
                             if k.lower() not in ('cookie', 'host', 'content-length')}
                )
                
                # Send response with status code
                self.send_response(response.status_code)
                
                # Send headers, including cookies
                for header, value in response.headers:
                    self.send_header(header, value)
                self.end_headers()
                
                # Send response body
                self.wfile.write(response.data)
                
        except Exception as e:
            print(f"Error handling GET request: {e}")
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Server Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    .error {{ background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <h1>Server Error</h1>
                <div class="error">
                    <p>An error occurred while processing your request. Please try again later.</p>
                    <p>Error details: {str(e)}</p>
                </div>
            </body>
            </html>
            """
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
            
            # Extract cookies from request headers
            cookies = {}
            if 'Cookie' in self.headers:
                cookie_header = self.headers['Cookie']
                cookie_parts = cookie_header.split('; ')
                for part in cookie_parts:
                    if '=' in part:
                        name, value = part.split('=', 1)
                        cookies[name] = value
            
            # Handle the POST request using Flask's test client
            with app.test_client() as test_client:
                # Set cookies in the test client
                for name, value in cookies.items():
                    test_client.set_cookie('', name, value)
                
                # Map the request to Flask
                content_type = self.headers.get('Content-Type', '')
                response = test_client.post(
                    self.path,
                    data=post_data,
                    content_type=content_type,
                    headers={k: v for k, v in self.headers.items() 
                             if k.lower() not in ('cookie', 'host', 'content-length')}
                )
                
                # Send response with status code
                self.send_response(response.status_code)
                
                # Send headers, including cookies
                for header, value in response.headers:
                    self.send_header(header, value)
                self.end_headers()
                
                # Send response body
                self.wfile.write(response.data)
                
                # Debug output for login requests
                if '/login' in self.path:
                    print(f"Login response status: {response.status_code}")
                    if 'Set-Cookie' in response.headers:
                        print(f"Login response contains cookies: {response.headers.get_all('Set-Cookie')}")
        except Exception as e:
            print(f"Error handling POST request: {e}")
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Server Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    .error {{ background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <h1>Server Error</h1>
                <div class="error">
                    <p>An error occurred while processing your request. Please try again later.</p>
                    <p>Error details: {str(e)}</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(error_message.encode('utf-8'))
        return