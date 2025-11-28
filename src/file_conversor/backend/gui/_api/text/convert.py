# src/file_conversor/backend/gui/_api/text/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.text.convert_cmd import execute_text_convert_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle text converting."""
    logger.debug(f"Text convert thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    file_format: str = params['file-format']

    execute_text_convert_cmd(
        input_files=input_files,
        format=file_format,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_text_convert():
    """API endpoint to convert text."""
    logger.info(f"[bold]{_('Text convert requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_text_convert",
    "EXTERNAL_DEPENDENCIES",
]
