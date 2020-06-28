from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """This function handles the registration on the site"""
    if current_user.is_authenticated:       # If the current user is already authenticated 
        return redirect(url_for('main.home'))    # Return user to home 
    form = RegistrationForm()  # Instance of the RegistrationForm class
    if form.validate_on_submit(): # If form is successfully validated upon submit
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # create a hashed password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)   # Store user details in 'user'
        db.session.add(user)
        db.session.commit()     # Commit changes to the database
        flash(f'Account created for {form.username.data}!', 'success') # flash this message 
        return redirect(url_for('users.login')) # redirect to login page
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """This function Handles the logins"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():   # Validate this form upon submit
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # If user exists and the password entered is valid
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')    # get next page
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # Return to the next page if it exits else return home
        else:
            flash('Login Unsuccesful! Recheck your email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """Logout Route"""
    logout_user()       # Logs out a user
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """This function handles account updates"""
    form = UpdateAccountForm()
    if form.validate_on_submit():       # Validate the form upon submit
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file  # Update the picture
        current_user.username = form.username.data  # Get the new username from the username field
        current_user.email = form.email.data    # Get the new email from the email field
        db.session.commit()   # Commit the changed username and email to the database
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))     # Return to home
        """The 3 lines of code below ensures that the username and email of the current user alreadey populates their respective fields"""
    elif request.method == 'GET':
        form.username.data = current_user.username  
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/home/<string:username>')
@login_required
def user_posts(username):
    """"This function handles a specific user's posts"""
    page = request.args.get('page', 1, type=int)    # Request for a page
    user = User.query.filter_by(username=username).first_or_404()   # Query the database and return the user
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)    # order posts by decending order
    return render_template('user_posts.html', posts=posts, user=user)   



@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """This function handles the request for password reset"""
    if current_user.is_authenticated:   # the two lines below ensures that the user is not logged in
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """This function handles the actual password reset"""
    if current_user.is_authenticated:   # the two lines below ensures that the user is not logged in
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an expired or invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): # If form is successfully validated upon submit
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # create a hashed password
        user.password = hashed_password
        db.session.commit()     # Commit changes to the database
        flash('Your password has been updated', 'success') # flash this message 
        return redirect(url_for('users.login')) # redirect to login page
    return render_template('reset_token.html', title='Reset Password', form=form)