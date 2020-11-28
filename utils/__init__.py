"""
import flask
from flask_login import LoginManager
from flask import Flask, render_template
from flask_wtf import CsrfProtect

app = Flask(__name__)

login = LoginManager(app)

"""