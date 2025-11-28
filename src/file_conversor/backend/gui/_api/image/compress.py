# src/file_conversor/backend/gui/_api/image/blur.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.compress_cmd import execute_image_compress_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image compression."""
    logger.debug(f"Image compress thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    quality = int(params.get('quality') or 100)

    execute_image_compress_cmd(
        input_files=input_files,
        quality=quality,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_compress():
    """API endpoint to compress image files."""
    logger.info(f"[bold]{_('Image compress requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_compress",
]
