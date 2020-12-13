from flask import Blueprint, render_template, redirect, flash
from views.forms import ForgotForm
from utils.models import User
from flask_login import current_user

mod = Blueprint("forgot_password", __name__)


@mod.route("/forgot", methods=['GET', 'POST'])
def forgot_password():

    # Logged in? Send to home screen
    if current_user.is_authenticated:
        return redirect('/')

    form = ForgotForm()
    if form.validate_on_submit():
        user = User.get_user(form.email.data, email=True)

        # Clear field
        form.email.data = ""

        # Send the reset email
        email = user.email
        flash(f"Password reset instructions has been sent to {email}.")

    return render_template("forgotpassword.html", title='Forgot Password?', form=form)
