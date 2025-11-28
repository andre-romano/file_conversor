# src/file_conversor/backend/gui/_api/pdf/convert.py

from flask import json, render_template, request, url_for

from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.convert_cmd import execute_pdf_convert_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF compression."""
    logger.debug(f"PDF compression thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    file_format = str(params['file-format'])
    image_dpi = int(params['image-dpi'])
    password = params['password'] or None

    execute_pdf_convert_cmd(
        input_files=input_files,
        output_dir=output_dir,
        format=file_format,
        dpi=image_dpi,
        password=password,
        progress_callback=status.set_progress,
    )


def api_pdf_convert():
    """API endpoint to convert PDF documents."""
    logger.info(f"[bold]{_('PDF conversion requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_pdf_convert",
]
