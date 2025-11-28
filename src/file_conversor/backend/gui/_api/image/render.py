# src/file_conversor/backend/gui/_api/image/render.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.render_cmd import execute_image_render_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image rendering."""
    logger.debug(f"Image render thread received: {params}")

    logger.info(f"[bold]{_('Rendering image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    file_format = params['file-format']
    image_dpi = int(params['image-dpi'])

    execute_image_render_cmd(
        input_files=input_files,
        format=file_format,
        dpi=image_dpi,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_render():
    """API endpoint to render image files."""
    logger.info(f"[bold]{_('Image render requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_render",
]
