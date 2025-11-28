# src/file_conversor/backend/gui/_api/image/resize.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.resize_cmd import execute_image_resize_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image resizing."""
    logger.debug(f"Image resize thread received: {params}")

    logger.info(f"[bold]{_('Resizing image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    scale = params['image-scale'] or None
    resampling = str(params['image-resampling'])

    execute_image_resize_cmd(
        input_files=input_files,
        scale=scale,
        width=None,
        resampling=resampling,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_resize():
    """API endpoint to resize image files."""
    logger.info(f"[bold]{_('Image resize requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_resize",
]
