from flask import Blueprint, render_template

mod = Blueprint("view_registration", __name__)


@mod.route("/registration")

def view_registration_page():

    # TODO registration logic

    return render_template("registration.html")
