# src/file_conversor/backend/gui/_api/pdf/merge.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.utils import CommandManager, ProgressManager
from file_conversor.utils.validators import check_path_exists

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF merge."""
    logger.debug(f"PDF merge thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_file = Path(params['output-file'])

    password = str(params['password']) or None

    logger.info(f"[bold]{_('Merging PDF files')}[/]...")
    output_file = output_file if output_file else Path() / CommandManager.get_output_file(input_files[0], stem="_merged")
    if not STATE["overwrite-output"]:
        check_path_exists(output_file, exists=False)

    backend = PyPDFBackend(verbose=STATE["verbose"])
    with ProgressManager() as progress_mgr:
        print(f"Processing '{output_file}' ...")
        backend.merge(
            # files
            input_files=input_files,
            output_file=output_file,
            password=password,
            progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p)),
        )
        status.set_progress(progress_mgr.complete_step())

    logger.debug(f"{status}")


def api_pdf_merge():
    """API endpoint to merge PDF documents."""
    logger.info(f"[bold]{_('PDF merge requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
