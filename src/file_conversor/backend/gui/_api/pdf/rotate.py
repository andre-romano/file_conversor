# src/file_conversor/backend/gui/_api/pdf/rotate.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.rotate_cmd import execute_pdf_rotate_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF rotate."""
    logger.debug(f"PDF rotate thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    password = params['password'] or None
    rotation = [f"1-:{params['rotation']}"]

    execute_pdf_rotate_cmd(
        input_files=input_files,
        rotation=rotation,
        password=password,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_pdf_rotate():
    """API endpoint to rotate PDF files."""
    logger.info(f"[bold]{_('PDF rotate requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_pdf_rotate",
    "EXTERNAL_DEPENDENCIES",
]
