from flask import render_template, Blueprint, flash, redirect
from .forms import LoginForm
# ...
mod = Blueprint("login", __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # do stuff to log user in instead of flashing their username
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)