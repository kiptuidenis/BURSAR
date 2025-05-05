from celery import Celery
from datetime import datetime
from sqlalchemy import and_
from ..models import User, Transaction
from ..services.mpesa_service import MPESAService
from app import create_app, db

# Initialize Celery
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def process_daily_transfers():
    """Process daily MPESA transfers for all users"""
    app = create_app()
    
    with app.app_context():
        current_time = datetime.now().time()
        
        # Get all users scheduled for current time
        users = User.query.filter(
            and_(
                User.transfer_time <= current_time,
                User.daily_limit > 0,
                User.active == True
            )
        ).all()
        
        mpesa_service = MPESAService()
        
        for user in users:
            try:
                # Calculate daily budget based on categories
                daily_total = sum(cat.daily_amount for cat in user.budget_categories if cat.active)
                
                # Don't exceed daily limit
                amount_to_transfer = min(daily_total, user.daily_limit)
                
                if amount_to_transfer > 0:
                    result = mpesa_service.initiate_b2c_payment(
                        phone_number=user.phone_number,
                        amount=amount_to_transfer
                    )
                    
                    if result['success']:
                        # Log successful transfer initiation
                        app.logger.info(f"Daily transfer initiated for user {user.id}: KES {amount_to_transfer}")
                    else:
                        app.logger.error(f"Failed to initiate transfer for user {user.id}: {result['error']}")
                        
            except Exception as e:
                app.logger.error(f"Error processing daily transfer for user {user.id}: {str(e)}")
                continue

@celery.task
def check_pending_transactions():
    """Check status of pending MPESA transactions"""
    app = create_app()
    
    with app.app_context():
        pending_transactions = Transaction.query.filter_by(status='pending').all()
        mpesa_service = MPESAService()
        
        for transaction in pending_transactions:
            try:
                status = mpesa_service.check_transaction_status(transaction.mpesa_reference)
                
                if status.get('ResultCode') == '0':
                    transaction.status = 'completed'
                elif status.get('ResultCode') in ['1', '2']:  # Failed or timeout
                    transaction.status = 'failed'
                    
                db.session.commit()
                
            except Exception as e:
                app.logger.error(f"Error checking transaction {transaction.id}: {str(e)}")
                continue