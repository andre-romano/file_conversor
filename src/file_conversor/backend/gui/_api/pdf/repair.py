# src/file_conversor/backend/gui/_api/pdf/repair.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Callable, Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.repair_cmd import execute_pdf_repair_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF repair."""
    logger.debug(f"PDF repair thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    password = params['password'] or None

    execute_pdf_repair_cmd(
        input_files=input_files,
        password=password,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_pdf_repair():
    """API endpoint to repair PDF files."""
    logger.info(f"[bold]{_('PDF repair requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_pdf_repair",
    "EXTERNAL_DEPENDENCIES",
]
