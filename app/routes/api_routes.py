from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
import json
from ..models import db, BudgetCategory, Transaction, User
from ..services.mpesa_service import MPESAService

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/mpesa/result', methods=['POST'])
def mpesa_result():
    """Handle MPESA B2C result callback"""
    result = request.get_json()
    
    # Find the transaction
    transaction = Transaction.query.filter_by(
        mpesa_reference=result.get('ConversationID')
    ).first()
    
    if transaction:
        if result.get('ResultCode') == '0':
            transaction.status = 'completed'
        else:
            transaction.status = 'failed'
            
        db.session.commit()
    
    return jsonify({'status': 'success'}), 200

@api_bp.route('/mpesa/deposit', methods=['POST'])
@login_required
def initiate_deposit():
    """Initiate M-Pesa STK Push for deposit"""
    from ..services.ngrok_tunnel import get_public_url
    
    # Try to get ngrok URL if in development
    base_url = current_app.config.get('BASE_URL')
    if current_app.debug:
        ngrok_url = get_public_url()
        if ngrok_url:
            base_url = ngrok_url
            current_app.logger.info(f"Using ngrok URL for callbacks: {base_url}")
    
    mpesa_service = MPESAService()
    
    try:
        # Set minimum deposit amount to 10 KES
        result = mpesa_service.initiate_stk_push(
            phone_number=current_user.phone_number,
            amount=10  # Minimum amount for testing
        )
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'message': 'Please check your phone for the M-Pesa prompt',
                'checkoutRequestID': result.get('CheckoutRequestID')
            })
        
        return jsonify({
            'success': False,
            'message': result.get('error', 'Failed to initiate deposit')
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error initiating deposit: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@api_bp.route('/mpesa/deposit/status/<checkout_request_id>')
@login_required
def check_deposit_status(checkout_request_id):
    """Check status of an STK Push request"""
    mpesa_service = MPESAService()
    
    try:
        result = mpesa_service.check_stk_push_status(checkout_request_id)
        
        if result.get('pending'):
            return jsonify({'pending': True})
            
        if result.get('ResultCode') == '0':
            # Transaction successful
            return jsonify({
                'success': True,
                'message': 'Deposit completed successfully'
            })
            
        return jsonify({
            'success': False,
            'message': result.get('ResultDesc', 'Transaction failed')
        })
        
    except Exception as e:
        current_app.logger.error(f"Error checking deposit status: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while checking the transaction status'
        }), 500

@api_bp.route('/mpesa/stk/callback', methods=['POST'])
def mpesa_stk_callback():
    """Handle MPESA STK Push callback"""
    try:
        data = request.get_json()
        current_app.logger.info(f"STK Callback received: {json.dumps(data)}")
        
        # Extract callback metadata
        callback_metadata = {}
        if 'Body' in data and 'stkCallback' in data['Body']:
            stk_callback = data['Body']['stkCallback']
            if stk_callback.get('ResultCode') == 0:
                # Transaction successful
                if 'CallbackMetadata' in stk_callback and 'Item' in stk_callback['CallbackMetadata']:
                    for item in stk_callback['CallbackMetadata']['Item']:
                        if item['Name'] == 'Amount':
                            callback_metadata['amount'] = item['Value']
                        elif item['Name'] == 'MpesaReceiptNumber':
                            callback_metadata['receipt_no'] = item['Value']
                        elif item['Name'] == 'PhoneNumber':
                            callback_metadata['phone_number'] = item['Value']
                
                # Find user by phone number
                phone = f"+{callback_metadata.get('phone_number')}"
                user = User.query.filter_by(phone_number=phone).first()
                
                if user and 'amount' in callback_metadata:
                    # Create deposit transaction
                    transaction = Transaction(
                        user_id=user.id,
                        amount=float(callback_metadata.get('amount')),
                        type='credit',
                        description=f"M-Pesa Deposit: {callback_metadata.get('receipt_no')}",
                        mpesa_reference=callback_metadata.get('receipt_no'),
                        status='completed'
                    )
                    
                    db.session.add(transaction)
                    db.session.commit()
                    
                    current_app.logger.info(f"Deposit recorded: {transaction}")
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error processing STK callback: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/budget/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if request.method == 'POST':
        data = request.get_json()
        
        category = BudgetCategory(
            name=data['name'],
            daily_amount=float(data['daily_amount']),
            user_id=current_user.id
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'id': category.id,
            'name': category.name,
            'daily_amount': category.daily_amount
        }), 201
    
    # GET method - return all categories
    categories = BudgetCategory.query.filter_by(
        user_id=current_user.id,
        active=True
    ).all()
    
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'daily_amount': cat.daily_amount
    } for cat in categories])

@api_bp.route('/budget/categories/<int:category_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_category(category_id):
    category = BudgetCategory.query.filter_by(
        id=category_id,
        user_id=current_user.id
    ).first_or_404()
    
    if request.method == 'DELETE':
        category.active = False
        db.session.commit()
        return '', 204
    
    # PUT method
    data = request.get_json()
    category.name = data.get('name', category.name)
    category.daily_amount = float(data.get('daily_amount', category.daily_amount))
    
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'daily_amount': category.daily_amount
    })

@api_bp.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'transactions': [{
            'id': t.id,
            'amount': t.amount,
            'type': t.type,
            'description': t.description,
            'status': t.status,
            'created_at': t.created_at.isoformat()
        } for t in transactions.items],
        'total_pages': transactions.pages,
        'current_page': transactions.page
    })