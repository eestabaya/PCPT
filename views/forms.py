import re
from utils.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        name = username.data
        sanitized = re.sub(r'\W+', '*', name)

        # Sanitize username, ensure it is alphanumeric with underscore
        if name is not sanitized:
            self.username.errors.append('Invalid username.')
            return False

        # Check if username is already being used
        user = User.get_user(name)
        if user is not None:
            self.username.errors.append('Username already in use.')
            return False
        return True

    def validate_email(self, email):
        user = User.get_user(email.data, email=True)
        if user is not None:
            self.email.errors.append('Email already in use.')
            return False
        return True


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password2', message='Passwords do not match.')])
    new_password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.get_user(email.data, email=True)
        if user is None:
            self.email.errors.append('Could not find account.')
            return False
        return True
