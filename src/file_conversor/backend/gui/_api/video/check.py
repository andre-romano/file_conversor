# src/file_conversor/backend/gui/_api/video/check.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.audio_video import FFprobeBackend

from file_conversor.utils import CommandManager, ProgressManager
from file_conversor.utils.backend import FFprobeParser

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle video checking."""
    logger.debug(f"Video check thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]

    logger.info(f"[bold]{_('Checking video files')}[/]...")
    backend = FFprobeBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        # display current progress
        parser = FFprobeParser(backend, input_file)
        parser.run()
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback)

    logger.debug(f"{status}")


def api_video_check():
    """API endpoint to check video files."""
    logger.info(f"[bold]{_('Video check requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
