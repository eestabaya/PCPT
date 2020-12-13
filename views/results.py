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

# TODO PLACEHOLDER STUFF MOCK TEST OF SEARCH
    temp = {
        "query": "radeon",
        "products_found": 7,
        "brandnames": ["Nvidia","Intel"],
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

    # TODO may display some sort of error
    if query is None or query is "" or query.isspace():
        return render_template("searchresults.html", user=user, var=temp)

    # Update user search history
    if user is not None:
        update_user(user.name, search=query)

    data = get_from_mongo(col="product")
    data = data["items"]
    items = []

    # TODO fix this shit
    for item in data:
        print(item)
        try:
            if query.lower() in item["_id"].lower():
                items.append(item)
        except:
            continue

    

    return render_template("searchresults.html", user=user, var=items, query=query, query_size=len(items))
