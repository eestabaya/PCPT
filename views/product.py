from flask import Blueprint, render_template

mod = Blueprint("view_product_page", __name__)


@mod.route("/product")

def view_product_page():

    # TODO product page logic

    return render_template("product.html")
