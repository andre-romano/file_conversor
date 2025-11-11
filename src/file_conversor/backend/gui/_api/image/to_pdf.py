# src/file_conversor/backend/gui/_api/image/to_pdf.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.image import Img2PDFBackend

from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.utils import CommandManager, ProgressManager
from file_conversor.utils.validators import check_path_exists

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

    logger.info(f"[bold]{_('Converting image files to PDF')}[/]...")
    input_files = [Path(i) for i in params['input-files']]
    output_file = Path(params.get('output-file') or "")

    image_dpi = int(params['image-dpi'])
    image_fit = params['image-fit']
    image_page_size = params['image-page-size']
    image_set_metadata = params['image-set-metadata']

    backend = Img2PDFBackend(
        verbose=STATE["verbose"],
    )

    if not STATE["overwrite-output"]:
        check_path_exists(output_file, exists=False)

    with ProgressManager() as progress_mgr:
        if image_page_size is None:
            page_sz = None
        elif image_page_size in Img2PDFBackend.PAGE_LAYOUT:
            page_sz = Img2PDFBackend.PAGE_LAYOUT[image_page_size]
        else:
            page_sz = tuple(image_page_size)

        backend.to_pdf(
            input_files=input_files,
            output_file=output_file,
            dpi=image_dpi,
            image_fit=Img2PDFBackend.FIT_MODES[image_fit],
            page_size=page_sz,
            include_metadata=image_set_metadata,
        )
        status.set_progress(progress_mgr.complete_step())

    logger.debug(f"{status}")


def api_image_to_pdf():
    """API endpoint to convert image files to PDF."""
    logger.info(f"[bold]{_('Image to PDF requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
