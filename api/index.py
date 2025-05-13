from flask import Flask, send_from_directory, render_template, redirect, url_for
from http.server import BaseHTTPRequestHandler
import os
import sys
import traceback

# Set up root path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Create Flask app with correct static folder
app = Flask(__name__, 
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static'),
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'templates')
)

# Configure app settings
app.debug = os.environ.get('DEBUG', 'False').lower() == 'true'
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-sessions')

# Register blueprints
try:
    from app.routes.user_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    print("Blueprints registered successfully")
except Exception as e:
    print(f"Error registering blueprints: {str(e)}")
    traceback.print_exc()

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, '..', 'app', 'static'),
        'favicon.ico',
        mimetype='image/x-icon'
    )

# Also handle favicon.png (some browsers request this)
@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(
        os.path.join(app.root_path, '..', 'app', 'static'),
        'favicon.png',
        mimetype='image/png'
    )

# Root route
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# Catch-all for static files
@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

# Define error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Vercel handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # We don't need to handle favicon separately anymore as Flask will handle it
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
            
            # Return a 500 error
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
