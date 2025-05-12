from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print("Login form submitted successfully") # Debug log
        # Handle phone number with or without country code
        phone = form.phone.data
        if not phone.startswith('+'):
            phone = '+254' + phone.lstrip('0')
        
        user = User.query.filter_by(phone_number=phone).first()
        
        if user and user.check_password(form.password.data):
            # Always use remember=True for serverless environments
            remember = True
                
            # Log the user in with strong session
            login_successful = login_user(user, remember=remember)
            print(f"Login attempt result: {login_successful}") # Debug log
            
            # Store additional auth info in session for redundancy
            from flask import session
            session['user_id'] = user.id
            session['authenticated'] = True
            session['user_phone'] = phone
            session.permanent = True
            
            print(f"User {user.id} logged in successfully with session: {session.items()}") # Debug log
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        
        print(f"Login failed for phone: {phone}") # Debug log
        flash('Invalid phone number or password', 'danger')
    else:
        print("Login form validation failed") # Debug log
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegistrationForm()  # Corrected indentation
    if form.validate_on_submit():
        print("Form validated successfully")  # Debug print
        phone = '+254' + form.phone.data
        if User.query.filter_by(phone_number=phone).first():
            print(f"Phone number {phone} already exists")  # Debug print
            flash('Phone number already registered', 'danger')
            return render_template('auth/register.html', form=form)
        
        # This block should be indented under "if form.validate_on_submit():"
        user = User(phone_number=phone)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    else: # This else corresponds to "if form.validate_on_submit():"
        print("Form validation failed")  # Debug print
        print("Form errors:", form.errors)  # Debug print to show validation errors
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))