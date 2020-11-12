from flask import Blueprint, render_template

mod = Blueprint("view_home", __name__)


@mod.route("/")
def home():
    stuff = {
        "x": 23,
        "y": "string",
        "z": ["this", "is", "a", "list"]
    }
    return render_template("index.html", var=stuff)
