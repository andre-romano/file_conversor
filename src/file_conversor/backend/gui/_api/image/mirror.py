# src/file_conversor/backend/gui/_api/image/mirror.py

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
    """Thread to handle image mirroring."""
    logger.debug(f"Image mirror thread received: {params}")

    logger.info(f"[bold]{_('Mirroring image files')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params.get('output-dir') or "")

    mirror_axis = params['mirror-axis']

    backend = PillowBackend(
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        backend.mirror(
            input_file=input_file,
            output_file=output_file,
            x_y=True if mirror_axis == "x" else False,
        )
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_mirrored")

    logger.debug(f"{status}")


def api_image_mirror():
    """API endpoint to mirror image files."""
    logger.info(f"[bold]{_('Image mirror requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
