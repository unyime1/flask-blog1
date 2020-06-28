"""This module handles the database"""
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # the TimedJSONWebSignatureSerializer is used to create tokens for password reset
from flaskblog import db, login_manager    # Imports the database and login manager from the __init__.py module. The app is needed because we need our applications secret key for password reset
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
    """Used to find users from the database by id"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """This class handles the user models"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(160), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """This function is used to create the secret token for password reset"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod       # Static methods are those that don't use the self variable but are in a class.
    def verify_reset_token(token):
        """This function verifies the password reset token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']     # Load token and get the user_id
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """This class handles the posts model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"