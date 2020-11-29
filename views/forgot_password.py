from flask import Blueprint, render_template

mod = Blueprint("forgot_password", __name__)


@mod.route("/forgot")
def view_forgot_password_page():
    # TODO forgot password logic
    return render_template("forgotpassword.html")
