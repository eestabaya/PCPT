from flask import Blueprint, render_template, request
from api.api import get_from_mongo

mod = Blueprint("view_results", __name__)


@mod.route("/search", methods=["POST"])
def process_results():

    # TODO this doesnt work
    if request.method != "POST":
        return render_template("searchresults.html")

    query = request.form['query']

    if query is "" or query.isspace():
        return render_template("searchresults.html")

    items = get_from_mongo()
    # TODO - if jquery is handled in python then this will be called every time, maybe keep it to js still?
    # pros - maybe it's easier? or is js easier?

    return render_template("searchresults.html", var=items)
