# src/file_conversor/backend/gui/_api/config.py

from flask import json, render_template, url_for

from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi, FlaskApiStatus

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def config_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """API endpoint to update the application configuration."""
    logger.info(f"[bold]{_('Configuration update requested via API.')}[/]")
    CONFIG.update(params)
    CONFIG.save()
    logger.debug(f"Configuration updated: {CONFIG}")


def api_config():
    """API endpoint to update the application configuration."""
    logger.info(f"[bold]{_('Configuration set requested via API.')}[/]")
    return FlaskApi.execute_response(config_thread)
