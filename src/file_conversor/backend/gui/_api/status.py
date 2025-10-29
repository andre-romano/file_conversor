# src/file_conversor/backend/gui/_api/status.py

from flask import json, render_template, request, url_for

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def api_status():
    """API endpoint to get the application status."""
    return FlaskApi.status_response(request.args.get('status_id'))
