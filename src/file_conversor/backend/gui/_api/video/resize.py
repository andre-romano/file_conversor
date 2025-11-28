# src/file_conversor/backend/gui/_api/video/resize.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.cli.video._ffmpeg_cmd import ffmpeg_cli_cmd, EXTERNAL_DEPENDENCIES

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
    """Thread to handle video resizing."""
    logger.debug(f"Video resize thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    file_format = params['file-format']

    audio_bitrate = params['audio-bitrate']
    video_bitrate = params['video-bitrate']

    video_encoding_speed = params['video-encoding-speed']
    video_quality = params['video-quality']

    resolution = params['resolution'] or None

    logger.info(f"[bold]{_('Resizing video files')}[/]...")
    ffmpeg_cli_cmd(
        input_files=input_files,
        file_format=file_format,

        audio_bitrate=audio_bitrate,
        video_bitrate=video_bitrate,
        video_encoding_speed=video_encoding_speed,
        video_quality=video_quality,

        resolution=resolution,

        output_dir=output_dir,
        out_stem="_resized",
        progress_callback=lambda p, pm: status.set_progress(pm.update_progress(p)),
    )

    logger.debug(f"{status}")


def api_video_resize():
    """API endpoint to resize video files."""
    logger.info(f"[bold]{_('Video resize requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_video_resize",
    "EXTERNAL_DEPENDENCIES",
]
