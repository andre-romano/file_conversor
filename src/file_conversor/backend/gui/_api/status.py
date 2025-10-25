# src/file_conversor/backend/gui/_api/status.py

from flask import json, render_template, request, url_for

# user-provided modules
from file_conversor.backend.gui.web_app import WebApp
from file_conversor.backend.gui.flask_status import FlaskStatus, FlaskStatusError, FlaskStatusUnknown

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
    # logger.info(f"[bold]{_('Status requested via API.')}[/]")
    status_id = request.args.get('status_id')
    # logger.debug(f"Status ID requested: {status_id} (type: {type(status_id)})")
    status = WebApp.get_instance().get_status(status_id)
    # if status.get_id() != '0':
    #     logger.debug(f"{status}")
    ret_code = 200
    if isinstance(status, FlaskStatusUnknown):
        ret_code = 404
    elif isinstance(status, FlaskStatusError):
        ret_code = 500
    return json.dumps(status.json()), ret_code
