# src/file_conversor/backend/gui/_api/video/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.cli.video._ffmpeg_cmd import ffmpeg_cli_cmd

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
    """Thread to handle video converting."""
    logger.debug(f"Video convert thread received: {params}")

    logger.info(f"[bold]{_('Converting video files')}[/]...")
    ffmpeg_cli_cmd(
        input_files=[Path(i) for i in params['input-files']],
        file_format=params['file-format'],
        audio_bitrate=int(params.get('audio-bitrate') or 0),
        video_bitrate=int(params.get('video-bitrate') or 0),
        audio_codec=params.get('audio-codec') or None,
        video_codec=params.get('video-codec') or None,
        video_encoding_speed=params.get('video-encoding-speed') or None,
        video_quality=params.get('video-quality') or None,
        resolution=params.get('resolution') or None,
        fps=params.get('fps') or None,
        brightness=params.get('brightness') or 1.0,
        contrast=params.get('contrast') or 1.0,
        color=params.get('color') or 1.0,
        gamma=params.get('gamma') or 1.0,
        rotation=params.get('rotation') or None,
        mirror_axis=params.get('mirror-axis') or None,
        deshake=params.get('deshake') or False,
        unsharp=params.get('unsharp') or False,
        output_dir=Path(params.get('output-dir') or ""),
        progress_callback=lambda p, pm: status.set_progress(pm.update_progress(p)),
    )

    logger.debug(f"{status}")


def api_video_convert():
    """API endpoint to convert video files."""
    logger.info(f"[bold]{_('Video convert requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
