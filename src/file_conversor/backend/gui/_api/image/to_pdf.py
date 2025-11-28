# src/file_conversor/backend/gui/_api/image/to_pdf.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.image.to_pdf_cmd import execute_image_to_pdf_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image to PDF conversion."""
    logger.debug(f"Image to PDF thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_file = Path(params['output-file'])

    image_dpi = int(params['image-dpi'])
    image_fit = str(params['image-fit'])
    image_page_size = params['image-page-size'] or None
    image_set_metadata = bool(params['image-set-metadata'])

    execute_image_to_pdf_cmd(
        input_files=input_files,
        dpi=image_dpi,
        fit=image_fit,
        page_size=image_page_size,
        set_metadata=image_set_metadata,
        output_file=output_file,
        progress_callback=status.set_progress,
    )


def api_image_to_pdf():
    """API endpoint to convert image files to PDF."""
    logger.info(f"[bold]{_('Image to PDF requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_to_pdf",
]
