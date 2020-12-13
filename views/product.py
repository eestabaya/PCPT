from flask import Blueprint, render_template, request
from flask_login import current_user
from api.api import get_product_from_mongo

mod = Blueprint("view_product", __name__)


@mod.route("/product", methods=["GET"])
def view_product_page():

    item_id = request.args.get('item_id')

    user = None
    if current_user.is_authenticated:
        user = current_user

    if item_id is None:
        return render_template("error.html", user=user), 404

    product_json = get_product_from_mongo(item_id)

    if product_json is None:
        return render_template("error.html", user=user), 404

    name = product_json["name"]
    rating = average_rating(product_json["stores"])
    img_url = product_json["picture"]

    if img_url is None:
        img_url = "https://slyce.it/wp-content/themes/unbound/images/No-Image-Found-400x264.png"

    stores = {}

    for site in product_json["stores"]:
        store_json = product_json["stores"][site]

        store_dict = {
            "store_url": store_json["link"],
            "product_price": store_json["price"],
            "store_iconurl": "https://c1.neweggimages.com/WebResource/Themes/logo_newegg_400400.png"
        }

        stores[site] = store_dict

    product = {
        "product_name": name,
        "product_rating": rating,
        "product_imgurl": img_url,
        "stores": stores
    }

    return render_template("product.html", product=product, user=user, item_id=item_id)


def average_rating(sites_dict):

    site_count = 0
    rating_sum = 0

    for site in sites_dict:
        site_count = site_count + 1
        rating_sum = rating_sum + sites_dict[site]["rating"]

    return int(rating_sum / site_count)
