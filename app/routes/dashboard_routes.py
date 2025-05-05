from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html',
                         daily_amount=current_user.daily_limit,
                         monthly_budget=current_user.monthly_limit,
                         balance=current_user.monthly_limit,  # This will be updated with actual balance calculation
                         categories=[],  # This will be populated when we implement budget categories
                         recent_transactions=[])  # This will be populated when we implement transactions

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handle profile updates
        current_user.transfer_time = request.form.get('transfer_time')
        current_user.monthly_limit = float(request.form.get('monthly_limit', 0))
        current_user.daily_limit = float(request.form.get('daily_limit', 0))
        current_user.two_factor_enabled = bool(request.form.get('enable_2fa'))
        
        # Update phone number if changed
        new_phone = '+254' + request.form.get('phone_number', '').strip()
        if new_phone != current_user.phone_number:
            if User.query.filter_by(phone_number=new_phone).first():
                flash('Phone number already registered', 'danger')
                return render_template('dashboard/profile.html')
            current_user.phone_number = new_phone
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        
    return render_template('dashboard/profile.html')