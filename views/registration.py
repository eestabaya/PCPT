from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_user
from utils.forms import RegistrationForm
from utils.models import User

from api.api import create_user


mod = Blueprint("view_registration", __name__)


@mod.route("/register", methods=["GET", "POST"])
def view_registration_page():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, pw=form.password.data)
        create_user(user)
        login_user(user)
        return redirect('/')
    return render_template("registration.html", title="Register", form=form)
