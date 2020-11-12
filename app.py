import uuid

import flask
from flask import Flask
from flask_wtf import CsrfProtect

from views import home
from api import api

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

registers = [
    home.mod,
    api.mod
]

for registration in registers:
    app.register_blueprint(registration)

CsrfProtect(app)


@app.errorhandler(404)
def page_not_found(e):
    return "Not found dummy", 404


@app.route('/js/<path:path>', methods=['GET'])
def assets(path):
    return flask.send_from_directory("static/js", path)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="127.0.0.1")
