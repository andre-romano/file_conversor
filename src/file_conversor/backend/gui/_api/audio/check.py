# src/file_conversor/backend/gui/_api/audio/check.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.audio.check_cmd import execute_audio_check_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle audio checking."""
    logger.debug(f"Audio check thread received: {params}")

    input_files: list[Path] = [Path(i) for i in params['input-files']]

    execute_audio_check_cmd(
        input_files=input_files,
        progress_callback=status.set_progress,
    )


def api_audio_check():
    """API endpoint to check audio files."""
    logger.info(f"[bold]{_('Audio check requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_audio_check",
]
