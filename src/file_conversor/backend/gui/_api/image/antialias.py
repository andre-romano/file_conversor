# src/file_conversor/backend/gui/_api/image/antialias.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.antialias_cmd import execute_image_antialias_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image antialiasing."""
    logger.debug(f"Image antialias thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    radius = int(params['radius'])
    algorithm = str(params['algorithm'])

    execute_image_antialias_cmd(
        input_files=input_files,
        radius=radius,
        algorithm=algorithm,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_antialias():
    """API endpoint to antialias image files."""
    logger.info(f"[bold]{_('Image antialias requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_antialias",
]
