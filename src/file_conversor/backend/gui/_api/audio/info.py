# src/file_conversor/backend/gui/_api/audio/info.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any
from datetime import timedelta

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.audio_video import FFprobeBackend

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_utils import *

from file_conversor.utils.formatters import format_bitrate, format_bytes

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _get_format_info(input_file: Path, format_info: dict):
    duration = format_info.get('duration', 'N/A')
    if duration != "N/A":
        duration_secs = int(float(duration))
        duration_td = timedelta(seconds=duration_secs)
        duration = str(duration_td)
    size = format_info.get("size", "N/A")
    if size != "N/A":
        size = format_bytes(float(size))
    bitrate = format_info.get('bit_rate', 'N/A')
    if bitrate != "N/A":
        bitrate = format_bitrate(int(bitrate))

    with div() as result:
        div(f"{_('File Information')}:")
        div(f"  - {_('Name')}: {input_file.name}")
        div(f"  - {_('Format')}: {format_info.get('format_name' 'N/A')}")
        div(f"  - {_('Duration')}: {duration}")
        div(f"  - {_('Size')}: {size}")
        div(f"  - {_('Bitrate')}: {bitrate}")
        br()
    return result


def _get_streams_info(input_file: Path, streams_info: list[dict]):
    with div() as result:
        div(f"{_("Media Streams")}:")
        for i, stream in enumerate(streams_info):
            stream_type = stream.get("codec_type", "unknown")
            codec = stream.get("codec_name", "N/A")
            resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}" if stream_type == "video" else ""
            bitrate = stream.get("bit_rate", "N/A")

            if bitrate != "N/A":
                bitrate = format_bitrate(int(bitrate))

            div(f"    {_('Stream')} #{i} ({stream_type.upper()}):")
            div(f"    - {_('Codec')}: {codec}")
            if resolution:
                div(f"    - {_('Resolution')}: {resolution}")
            div(f"    - {_('Bitrate')}: {bitrate}")
            if stream_type == "audio":
                div(f"    - {_('Sampling rate')}: {stream.get('sample_rate', 'N/A')} Hz")
                div(f"    - {_('Channels')}: {stream.get('channels', 'N/A')}")
            br()
        br()
    return result


def _get_chapters_info(input_file: Path, chapters_info: list[dict]):
    with div() as result:
        div(f"{_('Chapters')}:")
        for chapter in chapters_info:
            title = chapter.get('tags', {}).get('title', 'N/A')
            start = chapter.get('start_time', 'N/A')
            div(f"  - {title} ({_('Time')}: {start}s)")
    return result


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle audio information retrieval."""
    logger.debug(f"Audio info thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]

    ffprobe_backend = FFprobeBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    with div() as result:
        for input_file in input_files:
            logger.info(f"[bold]{_('Retrieving info for')}[/] [green]{input_file.name}[/]...")

            metadata = ffprobe_backend.info(input_file)
            if "format" in metadata:
                _get_format_info(input_file, metadata["format"])

            if "streams" in metadata and len(metadata["streams"]) > 0:
                _get_streams_info(input_file, metadata["streams"])

            if "chapters" in metadata and len(metadata["chapters"]) > 0:
                _get_chapters_info(input_file, metadata["chapters"])

            div("----------------------------------------")
            br()

    status.set_message(str(result))
    status.set_progress(100)
    logger.debug(f"{status}")


def api_audio_info():
    """API endpoint to get audio file information."""
    logger.info(f"[bold]{_('Audio info requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
