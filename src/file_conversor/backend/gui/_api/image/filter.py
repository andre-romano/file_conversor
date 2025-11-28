# src/file_conversor/backend/gui/_api/image/filter.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.filter_cmd import execute_image_filter_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image filtering."""
    logger.debug(f"Image filter thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    image_filters: list[str] = [params['filter']]

    execute_image_filter_cmd(
        input_files=input_files,
        filters=image_filters,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_filter():
    """API endpoint to filter image files."""
    logger.info(f"[bold]{_('Image filter requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_filter",
]
