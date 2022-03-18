from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import * 
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    form = RegistrationForm()
    if form.validate_on_submit():  # check for post data before returning a form
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # adding user
        db.session.commit()  # commiting changes
        flash('Your account has been created!', 'success')
        # url_for argument is the function not the route
        return redirect(url_for('users.login'))
    return render_template("register.html", title='Register', form=form)


@users.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # getting queries, args is dictionary, using get to prevent errors
            flash('Logged in Successfully', 'success')
            return redirect(url_for('users.account')) if next_page else redirect(url_for('main.hello')) # ternary
        else: 
            flash('Login unsuccesful, please enter valid email and password', 'danger')
    return render_template("login.html", title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.hello"))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if not form.picture.data and form.username.data == current_user.username and form.email.data == current_user.email:
            flash('Nothing to Update', 'info')
        else:
            if form.picture.data:
                picture_fn = save_picture(form.picture.data)
                current_user.image_file = picture_fn
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your profile is Updated!', 'success')
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('account.html', image_file=url_for('static', filename='profile_pics/'+current_user.image_file), form=form)
    
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Link sent to your email', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST']) # route with queries
def reset_token(token): # taking queries as args
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():  # check for post data before returning a form
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()  # commiting changes
        flash('Your password has been changed!', 'success')
        # url_for argument is the function not the route
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)