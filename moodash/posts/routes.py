from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post 
from flaskblog.posts.forms import CrPostForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CrPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created!", 'success')
        return redirect(url_for('main.hello'))
    return render_template('create_post.html', form=form)
