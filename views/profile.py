from flask import Blueprint, redirect, render_template, flash
from flask_login import current_user
from views.forms import ChangePasswordForm
from api.api import find_user

mod = Blueprint('view_profile', __name__)


@mod.route('/profile', methods=["GET", "POST"])
def view_profile_page():

    user = current_user

    if not user.is_authenticated:
        return redirect('/login')

    mongo_user = find_user(user.name)

    search_history = mongo_user["search_history"]

    # Truncate search history to past 9 searches
    if len(search_history) > 9:
        del search_history[9:]

    user_json = {
        "name": user.name,
        "email": user.email,
        "past_searches": search_history
    }

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not user.check_password(form.password.data):
            flash('Old password is incorrect!')
            return render_template("profile.html", user=user, data=user_json, form=form)

        # update password here

    return render_template("profile.html", user=user, data=user_json, form=form)
