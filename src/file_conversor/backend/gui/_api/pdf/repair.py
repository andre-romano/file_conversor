# src/file_conversor/backend/gui/_api/pdf/repair.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import PikePDFBackend

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation
from file_conversor.utils.rich_utils import get_progress_bar

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF repair."""
    logger.debug(f"PDF repair thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    password = str(params['password'])

    logger.info(f"[bold]{_('Performing PDF repair')}[/]...")
    pikepdf_backend = PikePDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ... ")
        pikepdf_backend.compress(
            # files
            input_file=input_file,
            output_file=output_file,

            # options
            decrypt_password=password,
            progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p)),
        )
        status.set_progress(progress_mgr.complete_step())
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_repaired")

    logger.debug(f"{status}")


def api_pdf_repair():
    """API endpoint to repair PDF files."""
    logger.info(f"[bold]{_('PDF repair requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
