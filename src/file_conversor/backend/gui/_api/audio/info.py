# src/file_conversor/backend/gui/_api/audio/info.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi, FlaskApiStatus
from file_conversor.backend.gui._api.video.info import _api_thread as _api_thread_info_video, EXTERNAL_DEPENDENCIES

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle audio information retrieval."""
    logger.debug(f"Audio info thread received: {params}")
    _api_thread_info_video(params, status)


def api_audio_info():
    """API endpoint to get audio file information."""
    logger.info(f"[bold]{_('Audio info requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_audio_info",
    "EXTERNAL_DEPENDENCIES",
]
