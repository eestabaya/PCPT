from flask import Blueprint, render_template, request
from flask_login import current_user

mod = Blueprint("view_product", __name__)


@mod.route("/product", methods=["GET"])
def view_product_page():

    item_id = request.args.get('id')

    user = None
    if current_user.is_authenticated:
        user = current_user
        # TODO do things as necessary

    #if item_id is None:
    #    return render_template("product.html", user=user)

    # # TODO return an error page if header is incomplete
    # if item_id is None:
    #     return render_template("error.html")

    # do some database stuff
    # get product from database using item id

    # # TODO return an error page if invalid product
    # item = "something"
    # if item is None:
    #     return render_template("error.html")

    # then return product!
    # placeholder below

    hierarchy = {

        # we found this from item_id
        "my_item_id": {
            "product_name": "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)",
            "product_description": "The XFX RX 580 series graphics card feature the latest Polaris architecture which includes the 4th gen GCN graphics cores, a brand new display engine, new multimedia cores, all on the revolutionary next finfet 14 process technology for enhanced performance and efficiency.",
            "product_rating": 3,
            "product_imgurl": "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg",
            "stores": {
                "Amazon": {
                    "store_url": "https://www.amazon.com/XFX-Radeon-1386MHz-Graphics-RX-580P8DFD6/dp/B06Y66K3XD/ref=sr_1_3?_encoding=UTF8&c=ts&dchild=1&keywords=Computer+Graphics+Cards&qid=1606706208&s=pc&sr=1-3&ts_id=284822",
                    "product_price": 199.99,
                    "product_in_stock": True,
                    "iconurl":"https://i.pinimg.com/originals/08/5f/d8/085fd8f7819dee3b716da73d3b2de61c.jpg",
                },

                "Adorama": {
                    "store_url": "https://www.amazon.com/XFX-Radeon-1386MHz-Graphics-RX-580P8DFD6/dp/B06Y66K3XD/ref=sr_1_3?_encoding=UTF8&c=ts&dchild=1&keywords=Computer+Graphics+Cards&qid=1606706208&s=pc&sr=1-3&ts_id=284822",
                    "product_price": 120.00,
                    "product_in_stock": False,
                    "store_iconurl": "https://res-3.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco/v1417180938/d4ed2k3yhq1dg3zs8kad.jpg"
                },
                
                "Newegg": {
                    "store_url": "https://www.newegg.com/xfx-radeon-rx-580-rx-580p8dfd6/p/N82E16814150803",
                    "product_price": 105.00,
                    "product_in_stock": True,
                    "store_iconurl": "https://c1.neweggimages.com/WebResource/Themes/logo_newegg_400400.png"
                }
            },
            "hist_price_data": 
            [
                {
                    "product_price": 20.99,
                    "date": "11/29/2020"
                },
                {
                    "product_price": 21.99,
                    "date": "11/30/2020"
                }
            ]
        }
    }

    return render_template("product.html", product=hierarchy["my_item_id"], user=user)
