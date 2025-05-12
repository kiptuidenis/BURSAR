from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Set up login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

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