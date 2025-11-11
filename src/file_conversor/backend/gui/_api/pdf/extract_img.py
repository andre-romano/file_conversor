# src/file_conversor/backend/gui/_api/pdf/extract_img.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import PyMuPDFBackend

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF image extraction."""
    logger.debug(f"PDF image extraction thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    logger.info(f"[bold]{_('Extracting images from PDF files')}[/]...")
    pymupdf_backend = PyMuPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pymupdf_backend.extract_images(
            # files
            input_file=input_file,
            output_dir=output_dir,
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=True)  # allow overwrite to avoid detecting PDF file as existing
    cmd_mgr.run(callback)

    logger.debug(f"{status}")


def api_pdf_extract_img():
    """API endpoint to extract images from PDF documents."""
    logger.info(f"[bold]{_('PDF image extraction requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
