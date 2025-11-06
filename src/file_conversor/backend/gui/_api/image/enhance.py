# src/file_conversor/backend/gui/_api/image/enhance.py

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
    """Thread to handle image enhancement."""
    logger.debug(f"Image enhance thread received: {params}")

    logger.info(f"[bold]{_('Enhancing image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params.get('output-dir') or "")

    color = float(params.get('color') or 1.0)
    brightness = float(params.get('brightness') or 1.0)
    contrast = float(params.get('contrast') or 1.0)
    sharpness = float(params.get('sharpness') or 1.0)

    backend = PillowBackend(
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        backend.enhance(
            input_file=input_file,
            output_file=output_file,
            color_factor=color,
            brightness_factor=brightness,
            contrast_factor=contrast,
            sharpness_factor=sharpness,
        )
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_enhanced")

    logger.debug(f"{status}")


def api_image_enhance():
    """API endpoint to enhance image files."""
    logger.info(f"[bold]{_('Image enhance requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
