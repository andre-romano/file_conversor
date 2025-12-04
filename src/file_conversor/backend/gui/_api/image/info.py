# src/file_conversor/backend/gui/_api/image/info.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.ocr_cmd import EXTERNAL_DEPENDENCIES

from file_conversor.utils.backend import PillowParser

from file_conversor.utils.dominate_utils import div

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

EXTERNAL_DEPENDENCIES = PillowParser.EXTERNAL_DEPENDENCIES


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle image info."""
    logger.debug(f"Image info thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]

    backend = PillowBackend(
        verbose=STATE["verbose"],
    )

    with div() as result:
        for input_file in input_files:
            logger.info(f"[bold]{_('Retrieving info for')}[/] [green]{input_file.name}[/]...")
            parser = PillowParser(backend, input_file)
            parser.run()

            parser.get_exif_info().div()

    status.set_message(str(result))
    status.set_progress(100)

    logger.debug(f"{status}")


def api_image_info():
    """API endpoint to get information about image files."""
    logger.info(f"[bold]{_('Image info requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_image_info",
]
