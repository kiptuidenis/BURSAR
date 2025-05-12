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
    
    try:
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
            
            # Add categories if user was created successfully
            try:
                categories = [
                    BudgetCategory(name='Food', daily_amount=100.0, user_id=admin.id),
                    BudgetCategory(name='Transport', daily_amount=50.0, user_id=admin.id),
                    BudgetCategory(name='Entertainment', daily_amount=30.0, user_id=admin.id)
                ]
                db.session.add_all(categories)  # Use add_all instead of bulk_save_objects
                db.session.commit()
                print("Categories added successfully")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding categories: {str(e)}")
            
            # Add sample transactions one by one with proper error handling
            try:
                timestamp1 = datetime.utcnow().timestamp()
                transaction1 = Transaction(
                    user_id=admin.id,
                    category_id=1,
                    amount=80.0,
                    type='debit',
                    description='Grocery shopping',
                    mpesa_reference=f'DEMO-REF-1-{timestamp1}',
                    status='completed'
                )
                db.session.add(transaction1)
                db.session.commit()
                print("Transaction 1 added successfully")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding transaction 1: {str(e)}")
            
            try:
                timestamp2 = datetime.utcnow().timestamp()
                transaction2 = Transaction(
                    user_id=admin.id,
                    category_id=2,
                    amount=30.0,
                    type='debit',
                    description='Taxi ride',
                    mpesa_reference=f'DEMO-REF-2-{timestamp2}',
                    status='completed'
                )
                db.session.add(transaction2)
                db.session.commit()
                print("Transaction 2 added successfully")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding transaction 2: {str(e)}")
            
            print("Database initialized with sample data")
        else:
            print("Database already initialized")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing database: {str(e)}")
