from flask import Blueprint, render_template, request

mod = Blueprint("view_product", __name__)


@mod.route("/product", methods=["GET"])
def view_product_page():

    item_id = request.args.get('id')
    print(request.args)

    # TODO return an error page if header is incomplete
    if item_id is None:
        return render_template("some_error_page_goes_here.html")

    # do some database stuff
    # get product from database using item id

    # TODO return an error page if invalid product
    item = "something"
    if item is None:
        return render_template("some_error_page_goes_here.html")

    # then return product!
    # placeholder below

    hierarchy = {

        # we found this from item_id
        "my_item_id": {
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

        "another item id": {}
    }

    return render_template("product.html", var=hierarchy["my_item_id"])
