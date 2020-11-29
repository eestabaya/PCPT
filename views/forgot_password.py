from flask import Blueprint, render_template
from .forms import ForgotForm

mod = Blueprint("forgot_password", __name__)


@mod.route("/forgot", methods=['GET', 'POST'])
def forgot_password():
    form = ForgotForm()
    # TODO forgot password logic
    return render_template("forgotpassword.html", title='Forgot Password?', form=form)
