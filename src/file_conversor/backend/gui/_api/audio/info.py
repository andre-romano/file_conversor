# src/file_conversor/backend/gui/_api/audio/info.py

import subprocess

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.audio_video import FFmpegBackend

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
    """Thread to handle audio information retrieval."""
    logger.debug(f"Audio info thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]

    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        # TODO
        pass

    logger.info(f"[bold]{_('Converting audio files')}[/]...")
    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback)

    logger.debug(f"{status}")


def api_audio_info():
    """API endpoint to get audio file information."""
    logger.info(f"[bold]{_('Audio info requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
