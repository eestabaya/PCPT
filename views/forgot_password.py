from flask import Blueprint, render_template

mod = Blueprint("view_password", __name__)


@mod.route("/password")

def view_forgot_password_page():

    # TODO comparison logic

    return render_template("password.html")