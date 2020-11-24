from flask import render_template, Blueprint, flash, redirect
from PCPT.views.forms import LoginForm
# ...
mod = Blueprint("login", __name__)

@mod.route('/login', methods=['GET', 'POST '])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)