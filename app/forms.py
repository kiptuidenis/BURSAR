from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20),
        Regexp(r'^[A-Za-z0-9_]+$', message="Username can only contain letters, numbers, and underscores")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
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
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')