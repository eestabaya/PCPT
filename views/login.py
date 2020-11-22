from flask_login import LoginManager
from flask import Blueprint, render_template, url_for, request, flash
#from app.forms import Login
from flask import request
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from utils.db_config import db

mod = Blueprint("login", __name__)
manager = LoginManager(mod)


class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        #return check_password_hash(password_hash, password) #TODO


    @manager.user_loader
    def load_user(self, u):
        u = db.Users.find_one({"Name": u})
        if not u:
            return None
        return User(username=u['Name'])


    @mod.route('/login', methods=['GET', 'POST'])
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = Login()
        if form.validate_on_submit():
            user = db.Users.find_one({"Name": form.name.data})
            if user and User.check_password(user['Password'], form.password.data):
                user_obj = User(username=user['Name'])
                login_user(user_obj)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            else:
                flash("Invalid username or password")
        return render_template('login.html', title='Sign In', form=form)


    @mod.route('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('login'))