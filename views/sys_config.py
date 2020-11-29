from flask import Blueprint, render_template

mod = Blueprint("view_sys_config", __name__)


@mod.route("/mysystemconfig")
# ensure user is logged in TODO
def view_config_page():

    # config hierarchy, collection will be "configurations"
    configurations = {

        "some_user_id": {
            "config_name": {
                "part1": {},
                "part2": {},
                "part3": {}
            },

            "my other config": {
                "part1": {},
                "part2": {},
                "part3": {}
            }
        },

        "another_user_id": {

        }
    }

    return render_template("configuration.html", var=stuff)
