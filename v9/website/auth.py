from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

# Functions for login, sign-up and logout.
# This function creates the route for the login page.
# Takes data from the login form.
# Validates that the email is registered.
# Checks that the password is correct.
# Redirecting to the blog/Q&A + Suggestions page.
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully! ✅', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('🚨 Incorrect password. Please try again.', category='error')
        else:
            flash('🚨 Email does not exist. Please try again.', category='error')

    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        if email_exists:
            flash('🚨 Email is already in use. Please use a different email.', category='error')
        # This line checks if the email does not end with @gmail.com.
        # Adding the other email to accept two different email types.
        elif not (email.endswith('@gmail.com') or email.endswith('@my.sanctamaria.school.nz')):
            flash('🚨 Email must end with @gmail.com or @my.sanctamaria.school.nz.', category='error')
        elif username_exists:
            flash('🚨 Username is already in use. Please use a different username.', category='error')
        elif password1 != password2:
            flash('🚨 Passwords do not match!', category='error')
        elif len(username) < 2:
            flash('🚨 Username must be greater than 1 character!', category='error')
        elif len(password1) < 8:
            flash('🚨 Password must be at least 8 characters!', category='error')
        elif len(email) < 4:
            flash('🚨 Email is invalid. Please try again.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='scrypt:32768:8:1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! ✅', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully! ✅', category='success')
    return redirect(url_for('auth.login'))