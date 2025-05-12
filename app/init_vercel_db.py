# Database initialization for in-memory SQLite on Vercel
import os
from datetime import datetime
from app import db
from app.models import User, BudgetCategory, Transaction

def init_vercel_db():
    """
    Initialize the in-memory database for Vercel environment
    This function creates tables and adds initial data
    """
    # Create all database tables
    db.create_all()
    
    # Add a default admin user if it doesn't exist
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            phone_number='+254700000000',
            active=True,
            monthly_limit=10000.0,
            daily_limit=500.0
        )
        admin.set_password('password123')
        db.session.add(admin)
        db.session.commit()
        
        # Add some default budget categories for the admin
        categories = [
            BudgetCategory(name='Food', daily_amount=100.0, user_id=admin.id),
            BudgetCategory(name='Transport', daily_amount=50.0, user_id=admin.id),
            BudgetCategory(name='Entertainment', daily_amount=30.0, user_id=admin.id)
        ]
        db.session.bulk_save_objects(categories)
        db.session.commit()
          # Add some sample transactions
        transactions = [
            Transaction(
                user_id=admin.id,
                category_id=1,
                amount=80.0,
                type='debit',
                description='Grocery shopping',
                mpesa_reference='',
                status='completed'
            ),
            Transaction(
                user_id=admin.id,
                category_id=2,
                amount=30.0,
                type='debit',
                description='Taxi ride',
                mpesa_reference='',
                status='completed'
            )
        ]
        db.session.bulk_save_objects(transactions)
        db.session.commit()
        
        print("Database initialized with sample data")
    else:
        print("Database already initialized")
