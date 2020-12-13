from flask import Blueprint, render_template
from flask_login import current_user

mod = Blueprint("home", __name__)


@mod.route("/")
def home():

    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)

    return render_template("index.html")
