from flask import Blueprint, redirect, render_template, flash
from flask_login import current_user
from views.forms import ChangePasswordForm
from api.api import find_user, update_user
from utils.models import User

mod = Blueprint('view_profile', __name__)


@mod.route('/profile', methods=["GET", "POST"])
def view_profile_page():

    user = current_user

    # Ensure logged in
    if not user.is_authenticated:
        return redirect('/login')

    # Access database to find search history
    mongo_user = find_user(user.name)
    search_history = mongo_user["search_history"]

    # Truncate search history to past 9 searches
    if len(search_history) > 9:
        del search_history[9:]

    name = user.name
    email = user.email

    user_json = {
        "name": name,
        "email": email,
        "past_searches": search_history
    }

    form = ChangePasswordForm()
    if form.validate_on_submit():

        # Validate old password
        if not user.check_password(form.old_password.data):
            flash('Old password is incorrect!')
            return render_template("profile.html", user=user, data=user_json, form=form)

        # Update password
        pw_tuple = user.set_password(form.new_password.data)
        salt = pw_tuple[0]
        hashed = pw_tuple[1]

        update_user(user.name, salt=salt, pw_hash=hashed)

        # Logout user for security
        flash('Password changed. You have been logged out for security purposes and may log in again.')
        return redirect('/logout')

    return render_template("profile.html", user=user, data=user_json, form=form)
