# src/file_conversor/backend/gui/_api/pdf/extract.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.utils import CommandManager, ProgressManager
from file_conversor.utils.formatters import parse_pdf_pages

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF page extraction."""
    logger.debug(f"PDF page extraction thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    pages = str(params['pages'])
    password = str(params['password']) or None

    logger.info(f"[bold]{_('Extracting pages from PDF files')}[/]...")
    backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        backend.extract(
            input_file=input_file,
            output_file=output_file,
            password=password,
            pages=parse_pdf_pages(pages),
            progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p))
        )
        status.set_progress(progress_mgr.complete_step())
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_extracted")

    logger.debug(f"{status}")


def api_pdf_extract():
    """API endpoint to extract pages from PDF documents."""
    logger.info(f"[bold]{_('PDF page extraction requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
