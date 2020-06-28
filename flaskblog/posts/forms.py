from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    """This class handles the posts to the site"""
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=50)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField("Post")