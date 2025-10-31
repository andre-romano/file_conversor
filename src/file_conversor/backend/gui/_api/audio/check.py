# src/file_conversor/backend/gui/_api/audio/check.py

import subprocess

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.audio_video import FFmpegBackend, FFprobeBackend

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def audio_check_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle audio checking."""
    logger.debug(f"Audio check thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input_files']]

    logger.info(f"[bold]{_('Checking audio files')}[/]...")
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        # display current progress
        ffmpeg_backend.set_files(input_file=input_file, output_file="-")
        try:
            ffmpeg_backend.execute(
                progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p))
            )
        except subprocess.CalledProcessError:
            logger.error(f"{_('FFMpeg check')}: [red][bold]{_('FAILED')}[/bold][/red]")
            raise RuntimeError(f"{_('File')} '{input_file}' {_('is corrupted or has inconsistencies')}")
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback)

    logger.debug(f"{status}")


def api_audio_check():
    """API endpoint to check audio files."""
    logger.info(f"[bold]{_('Audio check requested via API.')}[/]")
    return FlaskApi.execute_response(audio_check_thread)
