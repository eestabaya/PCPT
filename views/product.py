from flask import Blueprint, render_template

from views.comparison import view_comparison_page, add_comparison_page
from views.sys_config import view_config_page, add_config, create_config
import webbrowser
mod = Blueprint("view_product", __name__)


@mod.route("/product", methods["POST"])

def view_product_page(item):
    #if request.method != "POST":
     #   return render_template("product.html")
    #if item is null:
     #   return render_template("error.html")



    return render_template("product.html", item)

def add_comparison(item):
    #if item is null:
     #   return null
    return add_comparison_page(item)

def view_comparison():
    return view_comparison_page()

def buy_product(item):
    # if item is null:
    #   return null
    webbrowser.open(item.store_url)

def new_config(item):
    # if item is null:
    #   return null
    return create_config(item)

def add_to_config(item):
    # if item is null:
    #   return null
    return add_config(item)

def view_config():
    return view_config_page



