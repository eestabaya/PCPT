from flask import Blueprint, render_template, redirect
from views.forms import ForgotForm
from utils.models import User
from flask_login import current_user

mod = Blueprint("forgot_password", __name__)


@mod.route("/forgot", methods=['GET', 'POST'])
def forgot_password():

    if current_user.is_authenticated:
        return redirect('/')

    form = ForgotForm()
    if form.validate_on_submit():
        u = User.get_user(form.email.data, email=True)

        if u is None:
            # TODO - output that user doesn't exist
            return render_template("forgotpassword.html", title='Forgot Password?', form=form)

        # TODO process form

    return render_template("forgotpassword.html", title='Forgot Password?', form=form)
