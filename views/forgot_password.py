from flask import Blueprint, render_template

mod = Blueprint("view_password", __name__)


@mod.route("/password") # TODO this will probably need to change

def view_forgot_password_page():

    # TODO forgot password logic

    return render_template("password.html")