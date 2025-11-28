# src/file_conversor/backend/gui/_api/pdf/decrypt.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.decrypt_cmd import execute_pdf_decrypt_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF decryption."""
    logger.debug(f"PDF decryption thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])
    password = str(params['password'])

    execute_pdf_decrypt_cmd(
        input_files=input_files,
        password=password,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_pdf_decrypt():
    """API endpoint to decrypt PDF documents."""
    logger.info(f"[bold]{_('PDF decryption requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
