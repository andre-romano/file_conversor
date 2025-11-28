# src/file_conversor/backend/gui/_api/xls/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.xls.convert_cmd import execute_xls_convert_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle spreadsheet conversion."""
    logger.debug(f"Spreadsheet conversion thread received: {params}")

    input_files: list[Path] = [Path(f) for f in params['input-files']]
    output_dir: Path = Path(params['output-dir'])
    file_format: str = str(params['file-format'])

    execute_xls_convert_cmd(
        input_files=input_files,
        format=file_format,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_xls_convert():
    """API endpoint to convert spreadsheets."""
    logger.info(f"[bold]{_('Spreadsheet conversion requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_xls_convert",
    "EXTERNAL_DEPENDENCIES",
]
