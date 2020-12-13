import uuid
import flask
from flask import Flask, render_template
from flask_wtf import CSRFProtect

from api import api
from utils.models import User
from flask_login import LoginManager

from views import (
    home,
    results,
    sys_config,
    product,
    profile
)

from views import registration, login

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.secret_key = str(uuid.uuid4())

registers = [
    home.mod,
    api.mod,
    results.mod,
    sys_config.mod,
    registration.mod,
    product.mod,
    login.mod,
    profile.mod
]

for registration in registers:
    app.register_blueprint(registration)

CSRFProtect(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


@app.route('/templates/<path:path>', methods=['GET'])
def views(path):
    return flask.send_from_directory("templates", path)


@app.route('/js/<path:path>', methods=['GET'])
def assets(path):
    return flask.send_from_directory("static/js", path)


@login_manager.user_loader
def load_user(username):
    return User.get_user(username)


if __name__ == '__main__':
    debug = False
    app.run(debug=debug, port=8080, host="0.0.0.0")
