from flask import send_from_directory, render_template, redirect, url_for
from http.server import BaseHTTPRequestHandler
import os
import sys
import traceback

# Set up root path for imports
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root_dir)

# Import the app factory function
try:
    # Set environment variable for Vercel detection
    os.environ['VERCEL'] = '1'
    
    # Import the create_app function from the app package
    from app import create_app
    
    # Create the Flask application using the factory function
    app = create_app()
    
    print("Flask app created successfully with create_app()")
except Exception as e:
    print(f"Error creating Flask app: {str(e)}")
    traceback.print_exc()

# Add a fallback for favicon.ico in case the app factory doesn't handle it
@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(
            os.path.join(root_dir, 'app', 'static'),
            'favicon.ico',
            mimetype='image/x-icon'
        )
    except Exception as e:
        print(f"Error serving favicon: {str(e)}")
        return '', 204  # No content if favicon can't be served

# Also handle favicon.png (some browsers request this)
@app.route('/favicon.png')
def favicon_png():
    try:
        return send_from_directory(
            os.path.join(root_dir, 'app', 'static'),
            'favicon.png',
            mimetype='image/png'
        )
    except Exception as e:
        print(f"Error serving favicon.png: {str(e)}")
        return '', 204  # No content if favicon can't be served

# Vercel handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Special handling for favicon paths to avoid Flask error
            if self.path in ['/favicon.ico', '/favicon.png']:
                favicon_path = os.path.join(root_dir, 'app', 'static', 
                                          'favicon.ico' if self.path == '/favicon.ico' else 'favicon.png')
                if os.path.exists(favicon_path):
                    with open(favicon_path, 'rb') as f:
                        favicon_data = f.read()
                    
                    mime_type = 'image/x-icon' if self.path == '/favicon.ico' else 'image/png'
                    self.send_response(200)
                    self.send_header('Content-Type', mime_type)
                    self.send_header('Content-Length', str(len(favicon_data)))
                    self.end_headers()
                    self.wfile.write(favicon_data)
                    return
                else:
                    # Return no content for missing favicons
                    self.send_response(204)
                    self.end_headers()
                    return
            
            # Use Flask test client to process the request
            with app.test_client() as test_client:
                response = test_client.get(self.path)
                
                # Send the response status
                self.send_response(response.status_code)
                
                # Set response headers
                for header, value in response.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                
                # Send response body
                self.wfile.write(response.data)
        except Exception as e:
            # Log any errors
            print(f"Error handling GET request: {str(e)}")
            traceback.print_exc()
            
            # Return a 500 error with plain text
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Server error: {str(e)}".encode('utf-8'))
            
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers.get('content-length', 0))
            body = self.rfile.read(content_length)
            
            # Use Flask test client to process the request
            with app.test_client() as test_client:
                response = test_client.post(
                    self.path,
                    data=body,
                    headers=dict(self.headers)
                )
                
                # Send the response status
                self.send_response(response.status_code)
                
                # Set response headers
                for header, value in response.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                
                # Send response body
                self.wfile.write(response.data)
        except Exception as e:
            # Log any errors
            print(f"Error handling POST request: {str(e)}")
            traceback.print_exc()
            
            # Return a 500 error
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Server error: {str(e)}".encode('utf-8'))

# Run the app when in development mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
