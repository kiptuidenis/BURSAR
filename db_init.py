import os
from app import create_app, db
from app.models import User, BudgetCategory, Transaction

def init_db():
    app = create_app()
    
    with app.app_context():
        # Make sure the instance folder exists
        instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path, exist_ok=True)
            print(f"Created instance directory at {instance_path}")
        
        # Create all database tables
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")

if __name__ == '__main__':
    init_db()