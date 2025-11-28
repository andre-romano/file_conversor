# src/file_conversor/backend/gui/_api/pdf/merge.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.merge_cmd import execute_pdf_merge_cmd, EXTERNAL_DEPENDENCIES

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
    input_files = [Path(i) for i in params['input-files']]
    output_file = Path(params['output-file'])

    password = params['password'] or None

    execute_pdf_merge_cmd(
        input_files=input_files,
        password=password,
        output_file=output_file,
        progress_callback=status.set_progress,
    )


def api_pdf_merge():
    """API endpoint to merge PDF documents."""
    logger.info(f"[bold]{_('PDF merge requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_pdf_merge",
    "EXTERNAL_DEPENDENCIES",
]
