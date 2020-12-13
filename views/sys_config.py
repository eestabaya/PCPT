from flask import Blueprint, render_template, redirect, flash, request
from flask_login import current_user
from api.api import find_user, get_product_from_mongo, update_user

mod = Blueprint("view_sys_config", __name__)


@mod.route("/mysystemconfig")
def view_config_page():

    # Check if user is authenticated
    user = current_user
    if not user.is_authenticated:
        return redirect('/login')

    # Get all system configuration data for user in database
    mongo_user = find_user(user.name)
    user_config = mongo_user["configuration"]

    parts = {}
    for part in user_config:
        product = get_product_from_mongo(part)

        img_url = product["picture"]
        if img_url is None:
            img_url = "https://slyce.it/wp-content/themes/unbound/images/No-Image-Found-400x264.png"

        part_json = {
            "imgurl": img_url
        }
        parts[product["name"]] = part_json

    config_json = {
        "parts": parts
    }

    return render_template("configuration.html", user=user, configs=config_json)


@mod.route('/addtoconfig')
def add_part_to_config():

    # Check if user is authenticated
    user = current_user
    if not user.is_authenticated:
        return redirect('/')

    # Check if PC part exists
    item_id = request.args.get('item_id')

    if item_id is None:
        return redirect('/')

    product_json = get_product_from_mongo(item_id)

    if product_json is None:
        return redirect('/')

    update_user(user.name, pc_part=product_json["_id"])

    flash("Added part to config!")
    return redirect('/mysystemconfig')
