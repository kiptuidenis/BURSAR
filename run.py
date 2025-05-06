import os
from app import create_app, db
from app.models import User, BudgetCategory, Transaction

app = create_app()

# Ensure instance directory exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Create an application context before working with the database
with app.app_context():
    try:
        # Create database tables
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == '__main__':
    app.run(debug=True)