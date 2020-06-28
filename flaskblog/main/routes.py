from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """"Home Page Route"""
    page = request.args.get('page', 1, type=int)    # Request for a page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)    # order posts by decending order
    return render_template('home.html', posts=posts)    


@main.route('/about')
def about():
    """"About Page Route"""
    return render_template('about.html', title='About')