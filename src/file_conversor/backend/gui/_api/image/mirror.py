# src/file_conversor/backend/gui/_api/image/mirror.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.mirror_cmd import execute_image_mirror_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image mirroring."""
    logger.debug(f"Image mirror thread received: {params}")

    logger.info(f"[bold]{_('Mirroring image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    mirror_axis = params['mirror-axis']

    execute_image_mirror_cmd(
        input_files=input_files,
        axis=mirror_axis,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_image_mirror():
    """API endpoint to mirror image files."""
    logger.info(f"[bold]{_('Image mirror requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_mirror",
]
