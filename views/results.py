from flask import Blueprint, render_template, request
from api.api import get_from_mongo, update_user
from flask_login import current_user

mod = Blueprint("view_results", __name__)


@mod.route("/search", methods=["GET"])
def process_results():
    query = request.args.get('query')

    user = None
    if current_user.is_authenticated:
        user = current_user

    # Display error for bad query
    if query is None or query is "" or query.isspace():
        return render_template("error.html", user=user), 404

    # Update user search history
    if user is not None:
        update_user(user.name, search=query)

    data = get_from_mongo(col="product")
    data = data["items"]
    items = []

    for item in data:
        try:
            if query.lower() in item["name"].lower():
                items.append(item)
        except:
            continue

    products_arr = []
    brands = []

    for item in items:

        info_tuple = compute_ranges(item["stores"])
        picture = item["picture"]
        brand = item["name"].split(" ")[0]

        if brand not in brands:
            brands.append(brand)

        if item["picture"] is None:
            picture = "https://slyce.it/wp-content/themes/unbound/images/No-Image-Found-400x264.png"

        product = {
            "product_name": item["name"],
            "price_low": info_tuple[0],
            "price_high": info_tuple[1],
            "product_rating": info_tuple[2],
            "product_id": item["_id"],
            "product_url": "http://localhost/product?item_id=" + item["_id"],
            "imgurl": picture
        }

        products_arr.append(product)

    items_dict = {
        "query": query,
        "products_found": len(items),
        "brandnames": brands,
        "products": products_arr
    }

    return render_template("searchresults.html", user=user, var=items_dict, query=query, query_size=len(items))


def compute_ranges(sites_dict):
    low = -1
    high = -1

    rating_sum = 0
    site_count = 0

    for site in sites_dict:
        site_count = site_count + 1
        rating_sum = rating_sum + sites_dict[site]["rating"]

        price = sites_dict[site]["price"]

        if low == -1 or low > price:
            low = price

        if high == -1 or price > high:
            high = price

    return low, high, int(rating_sum / site_count)
