# src/file_conversor/backend/gui/_api/shutdown.py

from flask import json, render_template, url_for

# user-provided modules
from file_conversor.backend.gui.flask_app import FlaskApp

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def api_shutdown():
    """API endpoint to shut down the application."""
    logger.info(f"[bold]{_('Shutdown requested via API.')}[/]")
    FlaskApp.get_instance().stop()
    return json.dumps({
        'status': 'success',
        'message': 'Shutting down...',
    }), 200
