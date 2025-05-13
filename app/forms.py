from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

class RegistrationForm(FlaskForm):
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

class LoginForm(FlaskForm):
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^[0-9]{9}$', message="Please enter 9 digits without country code")
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')

class ProfileForm(FlaskForm):
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