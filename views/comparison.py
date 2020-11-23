from flask import Blueprint, render_template

mod = Blueprint("view_comparison", __name__)


@mod.route("/comparison")

def view_comparison_page():

    # TODO comparison logic

    return render_template("comparison.html")