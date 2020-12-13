from flask import Blueprint, render_template, redirect
from flask_login import current_user
from api.api import find_user

mod = Blueprint("view_sys_config", __name__)


@mod.route("/mysystemconfig")
def view_config_page():

    test_config = {
        "parts" : {
            "Intel® Core™ i9-10850K Processor (20M Cache, up to 5.20 GHz)" : {
                "imgurl" : "https://static.bhphoto.com/images/images1000x1000/1589327172_1558682.jpg"
            },
            "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 3xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)" : {
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            "LG 34WN80C-B 34 inch 21:9 Curved UltraWide WQHD IPS Monitor with USB Type-C Connectivity sRGB 99% Color Gamut and HDR10 Compatibility, Black (2019)" : {
                "imgurl" : "https://images-na.ssl-images-amazon.com/images/I/81WBbFOEHwL._AC_SL1500_.jpg"
            },
            "MSI Vigor GK40 Wired RGB Gaming Keyboard":{
                "imgurl" : "https://c1.neweggimages.com/ProductImage/23-167-020-V01.jpg"
            },
            "XFX Radeon RX 580 GTS XXX Edition 1386MHz OC+, 8GB GDDR5, VR Ready, Dual BIOS, 13xDP HDMI DVI, AMD Graphics Card (RX-580P8DFD6)" : {
                "imgurl" : "https://static.bhphoto.com/images/images2500x2500/1548869076_1456228.jpg"
            },
            "LG 34WN80C-B 34 inch 21:9 Curved UltraWide WQHD IPS Monitor with USB Type-C Co1nnectivity sRGB 99% Color Gamut and HDR10 Compatibility, Black (2019)" : {
                "imgurl" : "https://images-na.ssl-images-amazon.com/images/I/81WBbFOEHwL._AC_SL1500_.jpg"
            },
            "MSI Vigor GK40 Wired RGB Gaming Keybo1ard":{
                "imgurl" : "https://c1.neweggimages.com/ProductImage/23-167-020-V01.jpg"
            }
        }
    }
    


    # Check if user is authenticated
    user = current_user
    if not user.is_authenticated:
        return render_template("configuration.html", configs=test_config)

    # Get all system configuration data for user in database
    mongo_user = find_user(user.name)
    user_configs = mongo_user["configurations"]

    return render_template("configuration.html", user=user, configs=user_configs)
