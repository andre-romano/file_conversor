# src\file_conversor\backend\audio_video\ffprobe_backend.py

"""
This module provides functionalities for handling audio and video files using FFprobe.
"""

import json

from pathlib import Path
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.backend.audio_video.abstract_ffmpeg_backend import AbstractFFmpegBackend

from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_file_format

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFprobeBackend(AbstractFFmpegBackend):
    """
    FFprobeBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    """

    EXTERNAL_DEPENDENCIES: set[str] = {
        "ffprobe",
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 
        :param verbose: Verbose logging. Defaults to False.      

        :raises RuntimeError: if dependency is not found
        """
        super().__init__(install_deps=install_deps, verbose=verbose)

    def get_resolution(self, file_path: str | Path):
        metadata = self.info(file_path)
        if "streams" in metadata:
            for stream in metadata["streams"]:
                stream: dict[str, str]
                stream_type = stream.get("codec_type", "unknown").lower()
                if stream_type != "video":
                    continue
                width = int(stream.get('width', '0'))
                height = int(stream.get('height', '0'))
                return width, height if width > 0 and height > 0 else None, None
        return None, None

    def get_duration(self, file_path: str | Path) -> float:
        """
        Calculate file total duration (in secs), using `ffprobe`.

        :return: Total duration in seconds. Returns 0 if duration cannot be determined.
        """
        process = Environment.run(
            f'{self._ffprobe_bin}',
            f'-v',
            f'error',
            f'-show_entries',
            f'format=duration', '-of',
            f'default=noprint_wrappers=1:nokey=1',
            f'{file_path}',
        )
        duration_str = process.stdout.strip()
        try:
            return float(duration_str if duration_str else "0")
        except ValueError:
            return 0.0

    def info(self, file_path: str | Path) -> dict:
        """
        Get file metadata in JSON format

        result = {
            streams: [],
            chapters: [],
            format: {},
        }

        stream = {
            index,
            codec_name,
            codec_long_name,
            codec_type: audio|video,
            sampling_rate,
            channels,
            channel_layout: stereo|mono,
        }

        format = {
            format_name,
            format_long_name,
            duration,
            size,
        }

        :return: JSON object
        """
        result = Environment.run(
            f"{self._ffprobe_bin}",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            "-show_error",
            f"{file_path}",
        )
        return json.loads(result.stdout)


__all__ = [
    "FFprobeBackend",
]
