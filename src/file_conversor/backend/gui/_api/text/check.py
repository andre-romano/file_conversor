# src/file_conversor/backend/gui/_api/text/check.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend import TextBackend

from file_conversor.utils import CommandManager, ProgressManager

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

    text_backend = TextBackend(verbose=STATE["verbose"])
    logger.info(f"{_('Checking files')} ...")

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.check(
            input_file=input_file,
        )
    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=True)
    cmd_mgr.run(callback)

    logger.debug(f"{status}")


def api_text_check():
    """API endpoint to check text."""
    logger.info(f"[bold]{_('Text check requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
