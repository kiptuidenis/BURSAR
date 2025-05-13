from flask import Flask, Response
from http.server import BaseHTTPRequestHandler
import os

# Create Flask app
app = Flask(__name__)

# Import routes after app is created to avoid circular imports
from app.routes import *

# Configure app settings
app.debug = os.environ.get('DEBUG', 'False').lower() == 'true'

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests in Vercel's serverless environment"""
        with app.test_client() as test_client:
            response = test_client.get(self.path)
            self.send_response(response.status_code)
            
            # Set response headers
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            
            # Send response body
            self.wfile.write(response.data)
            return
            
    def do_POST(self):
        """Handle POST requests in Vercel's serverless environment"""
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)
        
        with app.test_client() as test_client:
            response = test_client.post(
                self.path,
                data=body,
                headers=dict(self.headers)
            )
            
            self.send_response(response.status_code)
            
            # Set response headers
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            
            # Send response body
            self.wfile.write(response.data)
            return

# Only run the application directly when in development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
