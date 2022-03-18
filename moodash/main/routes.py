from flask import Blueprint, render_template
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")   # same function for two routes, functions can return html
def hello():
    # passing variables to template
    posts = Post.query.all()
    return render_template("home.html", posts=posts, title="Welcome")


@main.route("/about")
def about():
    return render_template("about.html", aboutpage="hello, this is about page of website")
