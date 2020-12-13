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
            if query.lower() in item["_id"].lower():
                items.append(item)
        except:
            continue

    products_arr = []
    for item in items:
        rating = 5
        price_low = 4
        price_high = 4

        picture = item["picture"]

        if item["picture"] is None:
            picture = "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg" # TODO placeholder fix

        product = {
            "product_name": item["name"],
            "product_rating": rating,
            "price_low": price_low,
            "price_high": price_high,
            "product_id": item["_id"],
            "product_url": "http://35.166.98.59/product?item_id=" + item["_id"],
            "imgurl": picture
        }

        products_arr.append(product)


    """
    items_dict = {
        "query": query,
        "products_found": len(items),
        "brandnames": ["Nvidia", "Intel"],
        "models" : ["Model1", "Model2"],
        "products": [
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 3,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_in_stock": True,
                "product_id": 1,
                "product_url": "http://34.220.161.8/product",
                "model": "Nvidia",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 4,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_in_stock": True,
                "product_id": 2,
                "product_url": "http://34.220.161.8/product",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 2,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_in_stock": True,
                "product_id": 4,
                "product_url": "http://34.220.161.8/product",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 1,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_in_stock": True,
                "product_id": 3,
                "product_url": "http://34.220.161.8/product",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 5,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_in_stock": True,
                "product_id": 5,
                "product_url": "http://34.220.161.8/product",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 3,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_in_stock": True,
                "product_id": 6,
                "product_url": "http://34.220.161.8/product",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            {
                "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
                "product_rating": 4,
                "price_low": 100.00,
                "price_high": 201.99,
                "product_id": 7,
                "product_url": "http://34.220.161.8/product",
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            }
        ]
    }
    """

    # TODO adjust
    items_dict = {
        "query": query,
        "products_found": len(items),
        "brandnames": ["Nvidia", "Intel"],
        "models" : ["Model1", "Model2"],
        "products": products_arr
    }

    return render_template("searchresults.html", user=user, var=items_dict, query=query, query_size=len(items))
