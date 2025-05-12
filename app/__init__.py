from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from .config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
server_session = Session()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Check if we're in Vercel environment
    is_vercel = app.config.get('VERCEL', False) or 'VERCEL' in os.environ
    
    # Configure session for Vercel serverless environment
    if is_vercel:
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SESSION_PERMANENT'] = True
        app.config['SESSION_USE_SIGNER'] = True
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['REMEMBER_COOKIE_DURATION'] = 3600 * 24 * 30  # 30 days
        app.config['REMEMBER_COOKIE_SECURE'] = True
        app.config['REMEMBER_COOKIE_HTTPONLY'] = True
        app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
    else:
        # Configure session for local development
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SESSION_PERMANENT'] = True
        app.config['SESSION_USE_SIGNER'] = True
        # Don't use secure cookies in development
        app.config['SESSION_COOKIE_SECURE'] = False
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['REMEMBER_COOKIE_DURATION'] = 3600 * 24 * 30  # 30 days
        app.config['REMEMBER_COOKIE_SECURE'] = False
        app.config['REMEMBER_COOKIE_HTTPONLY'] = True
        app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
        
    # Initialize session after app config
    server_session.init_app(app)
    
    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Only initialize migrate in non-Vercel environments
    if not is_vercel:
        migrate.init_app(app, db)
        
    # Initialize CSRF with config-dependent settings
    csrf.init_app(app)    # Set up login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    login_manager.needs_refresh_message = 'Please login again to confirm your identity'
    login_manager.needs_refresh_message_category = 'info'
    
    # Configure for Vercel environment
    if is_vercel:
        login_manager.refresh_view = 'auth.login'

    # Register blueprints
    from .routes.user_routes import auth_bp
    from .routes.dashboard_routes import dashboard_bp
    from .routes.api_routes import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    # Add current_user to template context
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)    # Register main route
    @app.route('/')
    def home():
        return render_template('home.html')
    
    # Add health check endpoint for Vercel
    @app.route('/api/health')
    def health_check():
        return {"status": "ok", "message": "BURSAR API is running"}, 200
        
    # Add simple API test endpoint
    @app.route('/api/test')
    def test_api():
        return {"status": "ok", "message": "API test successful"}, 200

    return app