from flask import Blueprint, render_template

mod = Blueprint("view_sys_config", __name__)


@mod.route("/mysystemconfig")
# ensure user is logged in TODO
def view_config_page():

    stuff = {
        # get data from mongodb TODO
    }

    return render_template("configuration.html", var=stuff)
