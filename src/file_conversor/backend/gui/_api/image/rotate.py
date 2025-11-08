# src/file_conversor/backend/gui/_api/image/rotate.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image rotation."""
    logger.debug(f"Image rotate thread received: {params}")

    logger.info(f"[bold]{_('Rotating image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params.get('output-dir') or "")

    rotation = int(params['image-rotation'])
    resampling = params['image-resampling']

    backend = PillowBackend(
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        backend.rotate(
            input_file=input_file,
            output_file=output_file,
            rotate=rotation,
            resampling=PillowBackend.RESAMPLING_OPTIONS[resampling],
        )
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_rotated")

    logger.debug(f"{status}")


def api_image_rotate():
    """API endpoint to rotate image files."""
    logger.info(f"[bold]{_('Image rotate requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
