from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    """This Class Handles Registration""" 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=70)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), Length(min=6, max=70), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """This function ensures the uniqueness of the usernames"""
        user = User.query.filter_by(username=username.data).first() # Query the database and store the data in user if it exists
        if user:        # If username exists in database
            raise ValidationError('This username is already taken. Choose another.')    # Throw an error

    def validate_email(self, email):
        """This function ensures the uniqueness of the emails"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already used by another user. Use another one.')


class LoginForm(FlaskForm):
    """This Class Handles Login""" 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=70)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """This Class Handles Registration""" 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """This function ensures the uniqueness of the usernames"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() # Query the database and store the data in user if it exists
            if user:        # If username exists in database
                raise ValidationError('This username is already taken. Choose another.')    # Throw an error

    def validate_email(self, email):
        """This function ensures the uniqueness of the emails"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already used by another user. Use another one.')

class RequestResetForm(FlaskForm):
    """This class handles requests for the password reset form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """This method ensures that the email provided by the user actually exists in the database"""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No user exits with this email. You must create an account first!')


class ResetPasswordForm(FlaskForm):
    """This method handles the actual password reset"""
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=70)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), Length(min=6, max=70), EqualTo('password')])
    submit = SubmitField("Reset Password")