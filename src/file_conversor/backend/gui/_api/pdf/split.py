# src/file_conversor/backend/gui/_api/pdf/rotate.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.split_cmd import execute_pdf_split_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF split."""
    logger.debug(f"PDF split thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    password = params['password'] or None

    execute_pdf_split_cmd(
        input_files=input_files,
        password=password,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_pdf_split():
    """API endpoint to split PDF files."""
    logger.info(f"[bold]{_('PDF split requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_pdf_split",
    "EXTERNAL_DEPENDENCIES",
]
