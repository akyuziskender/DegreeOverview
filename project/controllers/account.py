from project import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from project.controllers.forms import LoginForm, RegistrationForm,DeleteUserForm
from project.config.crypto import Crypto
from project.models.models import RegUser, Department
from project.models.dbOperations import *

#route login
@app.route('/login', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = RegUser.query.filter_by(email=form.email.data+"@itu.edu.tr").first()
        if user and Crypto.checkPassword(form.password.data, user.password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html',form=form, title='Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods = ['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        if registerUser(form):
            flash('Your account has been created! You are now able to login.', 'success')
            return redirect(url_for('home'))
        else:
            flash('The email is already taken.')

    return render_template('register.html', form=form, title='Register')