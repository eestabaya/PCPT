from flask import Blueprint, redirect, render_template
from flask_login import current_user
from views.forms import ChangePasswordForm

mod = Blueprint('view_profile', __name__)


@mod.route('/profile')
def view_profile_page():

    user = current_user
    
    # do other things
    test_json = {
        "name": "John Doe",
        "email": "jdoe@ucsd.edu",
        "past_searches" : [
            "graphics card",
            "monitor",
            "keyboard"
        ]
    }

    form = ChangePasswordForm()

    if not user.is_authenticated:
        # return redirect('/login')
        return render_template("profile.html", user={"name": "John Doe", "email": "jdoe@ucsd.edu"}, data=test_json, form=form)

    user_json = {
        "name": user.name,
        "email": user.email,
        "past_searches" : [
            "graphics card",
            "monitor",
            "keyboard"
        ]
    }


    return render_template("profile.html", user=user, data=user_json, form=form)
