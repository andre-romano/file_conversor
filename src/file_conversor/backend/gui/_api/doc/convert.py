# src/file_conversor/backend/gui/_api/doc/convert.py

from flask import json, render_template, request, url_for

from typing import Any

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


def api_doc_convert():
    """API endpoint to convert documents."""
    logger.info(f"[bold]{_('Document conversion requested via API.')}[/]")
    # TODO
    return json.dumps({
        'status': 'processing',
        'message': 'Document conversion in progress.',
    }), 200
