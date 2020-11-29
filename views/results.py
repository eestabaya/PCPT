from flask import Blueprint, render_template, request
from api.api import get_from_mongo

mod = Blueprint("view_results", __name__)


@mod.route("/search", methods=["GET"])
def process_results():

    """
    # TODO this doesnt work
    if request.method != "POST":
        return render_template("searchresults.html")
    """

    # query = request.form['query']
    query = request.args.get('query')

    if query is None or query is "" or query.isspace():
        return render_template("searchresults.html")

    items = get_from_mongo()
    # TODO - if jquery is handled in python then this will be called every time, maybe keep it to js still?
    # pros - maybe it's easier? or is js easier?

    # another alternative, do js payload and read data from there? then jquery handles the rest

    print(items)
    for x in items['items']:
        print(x)

    # TODO PLACEHOLDER STUFF MOCK TEST OF SEARCH
    temp = {
        "part1": {
            "lmao": "zedong",
            "lmfao": "pepega"
        },
        "part2": {
            "pepe": "the frog",
            "this is": "a test?"
        },
        "another p": {
            "good game": "not"
        },
        "yes": {
            "hehe": "xd"
        },
    }



    # TODO here are some notes
        # take data, let results = {{ template }} <-- i honestly have no idea how to run this
        # load and json stuff up, jquery gets handled from there
    print(list(temp.keys()))
    return render_template("searchresults.html", var=list(temp.keys()), e=query)
