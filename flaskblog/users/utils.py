import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    """This function is used to resize and save the profile pictures on the site"""
    random_hex = secrets.token_hex(8)   # Makes a random hex of 8 characters
    _, f_ext = os.path.splitext(form_picture.filename) # Grap the file_extension of the image to be saved
    picture_fn = random_hex + f_ext     # Concatenate the random hex of the filename with the file extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)    # Specifies the full path to where the picture will be saved
    
    output_size = (125, 125)        # size in pixels
    i = Image.open(form_picture)
    i.thumbnail(output_size)    # Resize image to the output size
    i.save(picture_path)     # Save the picture to the picture_path
   
    return picture_fn


def send_reset_email(user):
    """This function handles the sending of reset tokens to user emails"""
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)