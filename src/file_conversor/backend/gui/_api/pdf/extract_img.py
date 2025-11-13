# src/file_conversor/backend/gui/_api/pdf/extract_img.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.extract_img_cmd import execute_pdf_extract_img_cmd

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF image extraction."""
    logger.debug(f"PDF image extraction thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    execute_pdf_extract_img_cmd(
        input_files=input_files,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )

    logger.debug(f"{status}")


def api_pdf_extract_img():
    """API endpoint to extract images from PDF documents."""
    logger.info(f"[bold]{_('PDF image extraction requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
