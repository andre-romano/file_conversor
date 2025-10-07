# src\file_conversor\gui\routes.py

from flask import render_template

# user-provided modules
from file_conversor.gui.flask_app import FlaskApp, FlaskRoute, CONFIG, STATE, LOG, get_translation

_ = get_translation()
logger = LOG.getLogger()


@FlaskRoute.register("/", methods=["GET"])
def index():
    return render_template("index.html", title="Home Page", user_name="Alice")
