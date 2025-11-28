# src/file_conversor/backend/gui/_api/image/unsharp.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.unsharp_cmd import execute_image_unsharp_cmd, EXTERNAL_DEPENDENCIES
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image unsharp."""
    logger.debug(f"Image unsharp thread received: {params}")

    logger.info(f"[bold]{_('Unsharping image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    radius = int(params['radius'])
    strength = int(params['image-unsharp-strength'])
    threshold = int(params['image-unsharp-threshold'])

    execute_image_unsharp_cmd(
        input_files=input_files,
        radius=radius,
        strength=strength,
        threshold=threshold,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_unsharp():
    """API endpoint to unsharp image files."""
    logger.info(f"[bold]{_('Image unsharp requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_unsharp",
]
