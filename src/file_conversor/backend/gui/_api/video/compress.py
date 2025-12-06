# src/file_conversor/backend/gui/_api/video/compress.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper, EXTERNAL_DEPENDENCIES

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
    """Thread to handle video compress."""
    logger.debug(f"Video compress thread received: {params}")

    logger.info(f"[bold]{_('Compressing video files')}[/]...")

    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    file_format = params['file-format']
    target_size = f"{params['target-size']}M"

    video_encoding_speed = params['video-encoding-speed']
    video_quality = params['video-quality']

    ffmpeg_cmd_helper = FFmpegCmdHelper(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # Set arguments for FFmpeg command helper
    ffmpeg_cmd_helper.set_input(input_files)
    ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_compressed", output_dir=output_dir)
    ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
    ffmpeg_cmd_helper.set_target_size(target_size)

    ffmpeg_cmd_helper.execute(
        progress_callback=lambda p, pm: status.set_progress(pm.update_progress(p)),
    )

    logger.debug(f"{status}")


def api_video_compress():
    """API endpoint to compress video files."""
    logger.info(f"[bold]{_('Video compress requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "api_video_compress",
    "EXTERNAL_DEPENDENCIES",
]
