from flask import Flask, Request
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import create_app

app = create_app()

# Required for Vercel
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set Flask app response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Create Flask app response
        with app.test_client() as test_client:
            response = test_client.get(self.path)
            
            # Send response back to client
            self.wfile.write(response.data)
            return
            
    def do_POST(self):
        # Get content length
        content_length = int(self.headers.get('Content-Length', 0))
        # Get request body
        request_body = self.rfile.read(content_length)
        
        # Set Flask app response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Create Flask app response
        with app.test_client() as test_client:
            response = test_client.post(
                self.path, 
                data=request_body,
                content_type=self.headers.get('Content-Type', '')
            )
            
            # Send response back to client
            self.wfile.write(response.data)
            return

# For local development
if __name__ == "__main__":
    app.run(debug=True)