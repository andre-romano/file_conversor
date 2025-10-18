# src/file_conversor/backend/gui/_api/status.py

from flask import json, render_template, request, url_for

# user-provided modules
from file_conversor.backend.gui.flask_app import FlaskApp
from file_conversor.backend.gui.flask_status import FlaskStatus

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
    logger.info(f"[bold]{_('Status requested via API.')}[/]")
    status_id = request.args.get('status_id')
    logger.debug(f"Status ID requested: {status_id} (type: {type(status_id)})")
    if status_id is None or status_id.lower() in ('', 'none', 'null', '0'):
        return FlaskStatus.get_status_ready().json(), 200
    status = FlaskApp.get_instance().get_status(status_id)
    if not status:
        return FlaskStatus.get_status_unknown(status_id).json(), 404
    return json.dumps(status.json()), 200
