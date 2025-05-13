from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, Form
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
import os

# Create a base form class that checks for Vercel environment
# If in Vercel, use regular Form without CSRF, otherwise use FlaskForm with CSRF
if os.environ.get('VERCEL') == '1':
    BaseForm = Form  # Use WTForms Form without CSRF for Vercel
    print("Using WTForms Form without CSRF for Vercel environment")
else:
    BaseForm = FlaskForm  # Use FlaskForm with CSRF for local development
    print("Using FlaskForm with CSRF for local environment")

class RegistrationForm(BaseForm):
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^[0-9]{9}$', message="Please enter 9 digits without country code")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$',
               message="Password must be at least 8 characters long and include both letters and numbers")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    terms = BooleanField('I agree to the Terms of Service', validators=[
        DataRequired(message="You must agree to the Terms of Service")
    ])

class LoginForm(BaseForm):
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^[0-9]{9}$', message="Please enter 9 digits without country code")
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')

class ProfileForm(BaseForm):
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^[0-9]{9}$', message="Please enter 9 digits without country code")
    ])
    username = StringField('Username')
    email = StringField('Email')
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password')
    monthly_limit = StringField('Monthly Limit', validators=[DataRequired()])
    daily_limit = StringField('Daily Limit', validators=[DataRequired()])
    transfer_time = StringField('Transfer Time', validators=[DataRequired()])
    enable_2fa = BooleanField('Enable Two-Factor Authentication')