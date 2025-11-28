# src/file_conversor/backend/gui/_api/pdf/ocr.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.ocr_cmd import execute_pdf_ocr_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF OCR."""
    logger.debug(f"PDF page OCR thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    languages = [str(params['pdf-language'])]

    execute_pdf_ocr_cmd(
        input_files=input_files,
        languages=languages,
        output_dir=output_dir,
    )


def api_pdf_ocr():
    """API endpoint to OCR PDF pages."""
    logger.info(f"[bold]{_('PDF page OCR requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_pdf_ocr",
    "EXTERNAL_DEPENDENCIES",
]
