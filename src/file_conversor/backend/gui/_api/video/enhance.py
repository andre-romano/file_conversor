# src/file_conversor/backend/gui/_api/video/enhance.py

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
    """Thread to handle video enhancing."""
    logger.debug(f"Video enhance thread received: {params}")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    file_format = params['file-format']

    audio_bitrate = params['audio-bitrate']
    video_bitrate = params['video-bitrate']

    video_encoding_speed = params['video-encoding-speed']
    video_quality = params['video-quality']

    resolution = params['resolution']
    fps = params['fps']

    brightness = params['brightness']
    contrast = params['contrast']
    color = params['color']
    gamma = params['gamma']

    deshake = params['deshake']
    unsharp = params['unsharp']

    logger.info(f"[bold]{_('Enhancing video files')}[/]...")
    ffmpeg_cli_cmd(
        input_files=input_files,
        file_format=file_format,

        audio_bitrate=audio_bitrate,
        video_bitrate=video_bitrate,
        video_encoding_speed=video_encoding_speed,
        video_quality=video_quality,

        resolution=resolution,
        fps=fps,

        brightness=brightness,
        contrast=contrast,
        color=color,
        gamma=gamma,

        deshake=deshake,
        unsharp=unsharp,

        output_dir=output_dir,
        out_stem="_enhanced",
        progress_callback=lambda p, pm: status.set_progress(pm.update_progress(p)),
    )

    logger.debug(f"{status}")


def api_video_enhance():
    """API endpoint to enhance video files."""
    logger.info(f"[bold]{_('Video enhance requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_video_enhance",
    "EXTERNAL_DEPENDENCIES",
]
