# src/file_conversor/backend/gui/_api/ebook/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.ebook.convert_cmd import execute_ebook_convert_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle ebook conversion."""
    logger.debug(f"Ebook conversion thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    file_format = str(params['file-format'])
    output_dir = Path(params['output-dir'])

    execute_ebook_convert_cmd(
        input_files=input_files,
        format=file_format,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )

    logger.debug(f"{status}")


def api_ebook_convert():
    """API endpoint to convert ebooks."""
    logger.info(f"[bold]{_('Ebook conversion requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_ebook_convert",
]
