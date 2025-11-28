# src/file_conversor/backend/gui/_api/text/compress.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.text.compress_cmd import execute_text_compress_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle text checking."""
    logger.debug(f"Text check thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    execute_text_compress_cmd(
        input_files=input_files,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_text_compress():
    """API endpoint to compress text."""
    logger.info(f"[bold]{_('Text compress requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_text_compress",
    "EXTERNAL_DEPENDENCIES",
]
