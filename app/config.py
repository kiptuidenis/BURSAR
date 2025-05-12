import os
import secrets
from datetime import timedelta
from pathlib import Path

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Get the absolute path to the project root directory
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Check if running in Vercel environment
    is_vercel = os.environ.get('VERCEL') == '1'
    
    # Define instance path
    instance_path = os.path.join(basedir, 'instance')
    
    # Only try to create directory if not in Vercel environment
    if not is_vercel:
        try:
            if not os.path.exists(instance_path):
                # Create directory with full permissions
                os.makedirs(instance_path, exist_ok=True)
                print(f"Created instance directory at {instance_path}")
                
            # Create session directory
            session_dir = os.path.join(instance_path, 'flask_session')
            if not os.path.exists(session_dir):
                os.makedirs(session_dir, exist_ok=True)
                print(f"Created session directory at {session_dir}")
        except Exception as e:
            print(f"Error creating directories: {e}")
    
    # Session file directory
    SESSION_FILE_DIR = os.path.join(instance_path, 'flask_session')
    
    # Database Configuration - use in-memory SQLite for Vercel
    if is_vercel:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        db_path = os.path.join(instance_path, 'app.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_TYPE = 'filesystem'  # Default session type
    
    # MPESA Configuration
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
    MPESA_API_URL = os.environ.get('MPESA_API_URL', 'https://sandbox.safaricom.co.ke')
    MPESA_BUSINESS_SHORTCODE = os.environ.get('MPESA_BUSINESS_SHORTCODE')
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
    MPESA_SECURITY_CREDENTIAL = os.environ.get('MPESA_SECURITY_CREDENTIAL')
    
    # Security Configuration
    WTF_CSRF_ENABLED = True