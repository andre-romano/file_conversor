# src/file_conversor/backend/gui/_api/config.py

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


def api_config():
    """API endpoint to update the application configuration."""
    logger.info(f"[bold]{_('Configuration update requested via API.')}[/]")
    data: dict[str, Any] = request.form.to_dict()
    logger.debug(f"Received data: {data}")
    # Update the configuration with the provided data
    for key, value in data.items():
        # Attempt to convert to appropriate type
        if value.lower() in ('true', 'on'):
            value = True
        elif value.lower() in ('false', 'off'):
            value = False
        elif value.lower() == 'none':
            value = None
        else:
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # Keep as string if conversion fails
        data[key] = value
    CONFIG.update(data)
    CONFIG.save()
    logger.debug(f"Configuration updated: {CONFIG}")
    return json.dumps({
        'status': 'success',
        'message': 'Configuration updated successfully.',
    }), 200
