from flask import Blueprint, redirect, render_template, flash
from flask_login import current_user, login_user, logout_user
from utils.models import User
import re

from views.forms import LoginForm

mod = Blueprint("login", __name__)


@mod.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        is_email = False

        email_reg = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.match(email_reg, form.username.data, re.IGNORECASE):
            is_email = True

        user = User.get_user(form.username.data, email=is_email)

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')

        login_user(user, remember=form.remember_me.data)
        return redirect('/')

    return render_template('login.html', title='Sign In', form=form)


@mod.route('/logout')
def logout():
    logout_user()
    return redirect('/')
