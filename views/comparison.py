from flask import Blueprint, render_template, request

mod = Blueprint("view_comparison", __name__)


@mod.route("/comparison")

def view_comparison_page():
    # TODO for each item, item_id[i] = 'id'
    item_id[0] = request.args.get('id')
    print(request.args)

    # TODO return an error page if header is incomplete
    if item_id[0] is None:
        return render_template("some_error_page_goes_here.html")

    # do some database stuff
    # get product from database using item id

    # TODO return an error page if invalid product
    item[0] = "something"
    if item[0] is None:
        return render_template("some_error_page_goes_here.html")

    # then return product!
    # placeholder below

    hierarchy = {

        # we found this from item_id
        "item_1_id": {
            "name": "",
            "something": "else",

            "websites": {

                "amazon": {
                    "link": "link here!",
                    "price?": "idk what else"
                },

                "adorama": {
                    "link": "link here!",
                    "price?": "idk what else"
                }
            }
        },

        "item_2_id": {}
    }

    return render_template("comparison.html", var=hierarchy["item_1_id", "item_2_id"])
