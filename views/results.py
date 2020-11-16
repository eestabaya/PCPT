from flask import Blueprint, render_template, request

mod = Blueprint("view_results", __name__)


@mod.route("/search", methods=["POST"])
def process_results():

    #TODO this doesnt work
    if request.method != "POST":
        return render_template("searchresults.html")

    search = request.form['query']

    if search is "" or search.isspace():
        return render_template("searchresults.html")

    stuff = {
        "x": search,
        "y": "string",
        "z": ["this", "is", "a", "list"]
    }
    return render_template("searchresults.html", var=stuff)
