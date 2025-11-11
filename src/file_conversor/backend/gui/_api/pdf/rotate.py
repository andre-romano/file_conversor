# src/file_conversor/backend/gui/_api/pdf/rotate.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation
from file_conversor.utils.formatters import parse_pdf_rotation
from file_conversor.utils.rich_utils import get_progress_bar

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF rotate."""
    logger.debug(f"PDF rotate thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    password = str(params['password'])
    rotation = [f"1-:{params['rotation']}"]

    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.rotate(
            input_file=input_file,
            output_file=output_file,
            decrypt_password=password,
            rotations=parse_pdf_rotation(rotation, pypdf_backend.len(input_file)),
            progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p))
        )
        status.set_progress(progress_mgr.complete_step())
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_rotated")

    logger.debug(f"{status}")


def api_pdf_rotate():
    """API endpoint to rotate PDF files."""
    logger.info(f"[bold]{_('PDF rotate requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
