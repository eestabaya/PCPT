from flask import Blueprint, render_template
from flask_login import current_user, login_required

mod = Blueprint("home", __name__)


@mod.route("/")
def home():
    stuff = {
        "x": 23,
        "y": "string",
        "z": ["this", "is", "a", "list"]
    }

    if current_user.is_authenticated:
        return render_template("index.html", var=stuff, user=current_user)

    return render_template("index.html", var=stuff)
