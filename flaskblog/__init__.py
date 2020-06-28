"""This is the main module"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy     # Database import
from flask_bcrypt import Bcrypt     # Hashing Algorithm
from flask_login import LoginManager    # Manages logins
from flask_mail import Mail
from flaskblog.config import Config



db = SQLAlchemy()        # Initializes the database
bcrypt = Bcrypt()        # Initializes the hashing algorithm
login_manager = LoginManager()   # Initializes the login manager
login_manager.login_view = 'users.login'  # Directs the code to where the login page is
login_manager.login_message_category = 'info'   # Sets the bootstrap alert category

mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app