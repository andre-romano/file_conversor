# src/file_conversor/backend/gui/_api/image/convert.py

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
    """Thread to handle video converting."""
    logger.debug(f"Video convert thread received: {params}")

    logger.info(f"[bold]{_('Converting video files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    format = params['file-format']
    output_dir = Path(params.get('output-dir') or "")

    quality = int(params.get('image-quality') or 100)

    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.convert(
            input_file=input_file,
            output_file=output_file,
            quality=quality,
        )
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.debug(f"{status}")


def api_image_convert():
    """API endpoint to convert image files."""
    logger.info(f"[bold]{_('Image convert requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
