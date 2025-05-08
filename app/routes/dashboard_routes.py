from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, BudgetCategory
from app.forms import ProfileForm

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    categories = BudgetCategory.query.filter_by(
        user_id=current_user.id,
        active=True
    ).all()
    
    return render_template('dashboard/index.html',
                         daily_amount=current_user.daily_limit,
                         monthly_budget=current_user.monthly_limit,
                         balance=current_user.monthly_limit,  # This will be updated with actual balance calculation
                         categories=categories,
                         recent_transactions=[])

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('dashboard.profile'))

        # Format phone number with country code
        phone = '+254' + form.phone_number.data
        
        # Check if phone number is taken by another user
        existing_user = User.query.filter_by(phone_number=phone).first()
        if existing_user and existing_user.id != current_user.id:
            flash('This phone number is already registered', 'danger')
            return redirect(url_for('dashboard.profile'))

        current_user.phone_number = phone
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.monthly_limit = float(form.monthly_limit.data)
        current_user.daily_limit = float(form.daily_limit.data)
        current_user.transfer_time = datetime.strptime(form.transfer_time.data, '%H:%M').time()
        current_user.two_factor_enabled = form.enable_2fa.data

        if form.new_password.data:
            current_user.set_password(form.new_password.data)

        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('dashboard.profile'))

    # Pre-fill form with current user data
    if request.method == 'GET':
        form.phone_number.data = current_user.phone_number[4:] if current_user.phone_number else ''
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.monthly_limit.data = str(current_user.monthly_limit or 0)
        form.daily_limit.data = str(current_user.daily_limit or 0)
        form.transfer_time.data = current_user.transfer_time.strftime('%H:%M') if current_user.transfer_time else '06:00'
        form.enable_2fa.data = current_user.two_factor_enabled

    return render_template('dashboard/profile.html', form=form)