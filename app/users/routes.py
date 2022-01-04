from flask import Blueprint, render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import RgistrationForm, LoginForm, UpdateAccountForm

users = Blueprint('users',__name__)

@users.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RgistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Creatd For User {form.username.data}!",'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title = "Sign Up", form = form)

@users.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True) ##remember=True can be taken from user input with a check box
            next_page = request.args.get("next") ## Get the url user was given before login
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Email Id and Password Not Match", "danger")
    return render_template('login.html', title = "Login", form = form)


#logout_user
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/useraccount", methods = ['GET', 'POST'])
@login_required
def useraccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated','success')
        return redirect(url_for('users.useraccount'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('useraccount.html', title = "User Account", form = form)


@users.route("/user/<string:username>")
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).all()
    title = f"{user.username}'s Posts"
    return render_template('user_post.html', posts = posts, title = title, user = user)