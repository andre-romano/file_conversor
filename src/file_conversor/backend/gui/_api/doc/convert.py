# src/file_conversor/backend/gui/_api/doc/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.doc.convert_cmd import execute_doc_convert_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def doc_convert_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle document conversion."""
    logger.debug(f"Document conversion thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])
    file_format = str(params['file-format'])

    execute_doc_convert_cmd(
        input_files=input_files,
        format=file_format,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_doc_convert():
    """API endpoint to convert documents."""
    logger.info(f"[bold]{_('Document conversion requested via API.')}[/]")
    return FlaskApi.execute_response(doc_convert_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_doc_convert",
]
