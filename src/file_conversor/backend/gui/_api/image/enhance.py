# src/file_conversor/backend/gui/_api/image/enhance.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.enhance_cmd import execute_image_enhance_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image enhancement."""
    logger.debug(f"Image enhance thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    color = float(params['color'])
    brightness = float(params['brightness'])
    contrast = float(params['contrast'])
    sharpness = float(params['sharpness'])

    execute_image_enhance_cmd(
        input_files=input_files,
        brightness=brightness,
        contrast=contrast,
        color=color,
        sharpness=sharpness,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_enhance():
    """API endpoint to enhance image files."""
    logger.info(f"[bold]{_('Image enhance requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_enhance",
]
