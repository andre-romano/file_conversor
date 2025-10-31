# src/file_conversor/backend/gui/_api/audio/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.cli.audio._ffmpeg_cmd import ffmpeg_audio_run

from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle audio converting."""
    logger.debug(f"Audio convert thread received: {params}")

    logger.info(f"[bold]{_('Converting audio files')}[/]...")
    ffmpeg_audio_run(
        input_files=[Path(i) for i in params['input-files']],
        file_format=params['file-format'],
        audio_bitrate=int(params.get('audio-bitrate', 0)),
        output_dir=Path(params.get('output-dir', "")),
        progress_callback=lambda p, pm: status.set_progress(pm.update_progress(p)),
    )

    logger.debug(f"{status}")


def api_audio_convert():
    """API endpoint to convert audio files."""
    logger.info(f"[bold]{_('Audio convert requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
