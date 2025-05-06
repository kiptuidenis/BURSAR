import os
import sys
from app import create_app, db
from app.models import User, BudgetCategory, Transaction

app = create_app()

def init_db():
    with app.app_context():
        # Ensure the instance directory exists
        instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path, exist_ok=True)
            print(f"Created instance directory at {instance_path}")

        # Remove existing database file if it exists
        db_path = os.path.join(instance_path, 'app.db')
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Removed existing database at {db_path}")
            except Exception as e:
                print(f"Error removing existing database: {e}")
                sys.exit(1)

        try:
            # Create all database tables
            db.create_all()
            print("Database initialized successfully!")
            print(f"Database created at: {db_path}")
        except Exception as e:
            print(f"Error initializing database: {e}", file=sys.stderr)
            print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)