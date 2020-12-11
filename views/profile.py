from flask import Blueprint, redirect, render_template
from flask_login import current_user
from views.forms import ChangePasswordForm
from api.api import find_user

mod = Blueprint('view_profile', __name__)


@mod.route('/profile')
def view_profile_page():

    user = current_user

    if not user.is_authenticated:
        return redirect('/login')

    mongo_user = find_user(user.name)

    user_json = {
        "name": user.name,
        "email": user.email,
        "past_searches": mongo_user["search_history"]
    }

    form = ChangePasswordForm()

    return render_template("profile.html", user=user, data=user_json, form=form)
