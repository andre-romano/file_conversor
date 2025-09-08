# src\file_conversor\backend\ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

import json
import re

from pathlib import Path
from datetime import timedelta
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_file_format

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager
from file_conversor.backend.abstract_backend import AbstractBackend, BackendOption

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegBackend(AbstractBackend):
    """
    FFmpegBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    """

    SUPPORTED_IN_AUDIO_FORMATS = {
        'aac': {},
        'ac3': {},
        'flac': {},
        'm4a': {},
        'mp3': {},
        'ogg': {},
        'opus': {},
        'wav': {},
    }
    SUPPORTED_IN_VIDEO_FORMATS = {
        '3gp': {},
        'asf': {},
        'avi': {},
        'flv': {},
        'h264': {},
        'hevc': {},
        'm4v': {},
        'mkv': {},
        'mov': {},
        'mp4': {},
        'mpeg': {},
        'mpg': {},
        'webm': {},
    }
    SUPPORTED_IN_FORMATS = SUPPORTED_IN_AUDIO_FORMATS | SUPPORTED_IN_VIDEO_FORMATS

    SUPPORTED_OUT_AUDIO_FORMATS = {
        'mp3': {
            "-f": BackendOption("-f", "mp3"),
            "-c:a": BackendOption("-c:a", "libmp3lame"),
            "-vn": BackendOption("-vn"),
        },
        'm4a': {
            "-f": BackendOption("-f", "ipod"),
            "-c:a": BackendOption("-c:a", "aac"),
            "-vn": BackendOption("-vn"),
        },
        'ogg': {
            "-f": BackendOption("-f", "ogg"),
            "-c:a": BackendOption("-c:a", "libvorbis"),
            "-vn": BackendOption("-vn"),
        },
        'opus': {
            "-f": BackendOption("-f", "opus"),
            "-c:a": BackendOption("-c:a", "libopus"),
            "-vn": BackendOption("-vn"),
        },
        'flac': {
            "-f": BackendOption("-f", "flac"),
            "-c:a": BackendOption("-c:a", "flac"),
            "-vn": BackendOption("-vn"),
        },
    }
    SUPPORTED_OUT_VIDEO_FORMATS = {
        'mp4': {
            "-f": BackendOption("-f", "mp4"),
            "-c:v": BackendOption("-c:v", "libx264"),
            "-c:a": BackendOption("-c:a", "aac"),
        },
        'avi': {
            "-f": BackendOption("-f", "avi"),
            "-c:v": BackendOption("-c:v", "mpeg4"),
            "-c:a": BackendOption("-c:a", "libmp3lame"),
        },
        'mkv': {
            "-f": BackendOption("-f", "matroska"),
            "-c:v": BackendOption("-c:v", "libx264"),
            "-c:a": BackendOption("-c:a", "aac"),
        },
        'webm': {
            "-f": BackendOption("-f", "webm"),
            "-c:v": BackendOption("-c:v", "libvpx"),
            "-c:a": BackendOption("-c:a", "libvorbis"),
        },
    }
    SUPPORTED_OUT_FORMATS = SUPPORTED_OUT_VIDEO_FORMATS | SUPPORTED_OUT_AUDIO_FORMATS

    SUPPORTED_AUDIO_CODECS = [
        "aac",
        "ac3",
        "flac",
        "libfdk_aac",
        "libmp3lame",
        "libopus",
        "libvorbis",
        "pcm_s16le",
    ]

    SUPPORTED_VIDEO_CODECS = [
        "h264_nvenc",
        "hevc_nvenc",
        "libvpx",
        "libvpx-vp9",
        "libx264",
        "libx265",
        "mpeg4",
    ]

    PROGRESS_RE = re.compile(r'time=(\d+):(\d+):([\d\.]+)')

    EXTERNAL_DEPENDENCIES = set([
        "ffmpeg",
        "ffprobe",
    ])

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the FFMpeg backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 
        :param verbose: Verbose logging. Defaults to False.      

        :raises RuntimeError: if ffmpeg dependency is not found
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "ffmpeg": "ffmpeg"
                }),
                BrewPackageManager({
                    "ffmpeg": "ffmpeg"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        # check ffprobe / ffmpeg
        self._ffprobe_bin = self.find_in_path("ffprobe")
        self._ffmpeg_bin = self.find_in_path("ffmpeg")

    def calculate_file_total_duration(self, file_path: str | Path) -> float:
        """
        Calculate file total duration (in secs), using `ffprobe`.

        :return: Total duration in seconds.
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
        return float(duration_str if duration_str else "0")

    def calculate_file_formatted_duration(self, file_path: str | Path) -> str:
        """
        Calculate file duration (formatted), using `ffprobe`.

        :return: Total duration  (format HH:MM:SS).
        """
        duration_secs = self.calculate_file_total_duration(file_path)

        # Convert seconds to timedelta and format as HH:MM:SS
        td = timedelta(seconds=int(duration_secs))
        return str(td)

    def get_file_info(self, file_path: str | Path) -> dict:
        """
        Executa ffprobe e retorna os metadados no formato JSON

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

    def _get_input_defaults(self, input_file: str | Path) -> list[BackendOption]:
        """
        Set the input file and check if it has a supported format.

        :param input_file: Input file path.

        :return: (Input file, in options).

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        # check file is found
        input_path = Path(input_file)
        if not input_path.exists() and not input_path.is_file():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # check if the input file has a supported format
        check_file_format(input_path, self.SUPPORTED_IN_FORMATS)

        # set the input format options based on the file extension
        in_ext = input_path.suffix[1:]
        if self.SUPPORTED_IN_FORMATS[in_ext]:
            return [opt for opt in self.SUPPORTED_IN_FORMATS[in_ext].values()]
        return []

    def _get_output_defaults(self, output_file: str | Path) -> list[BackendOption]:
        """
        Set the output file and check if it has a supported format.

        :param output_file: Output file path.

        :return: (Output file, out options).

        :raises typer.BadParameter: Unsupported format, or file not found.
        """
        output_path = Path(output_file)

        # create out dir (if it does not exists)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # check if the output file has a supported format
        check_file_format(output_path, self.SUPPORTED_OUT_FORMATS)

        # set the output format options based on the file extension
        out_ext = output_path.suffix[1:]
        if self.SUPPORTED_OUT_FORMATS[out_ext]:
            return [opt for opt in self.SUPPORTED_OUT_FORMATS[out_ext].values()]
        return []

    def _override_with(self, default_opts: list[BackendOption], user_opts: list[BackendOption]) -> list[str]:
        res: list[str] = []
        for opt in default_opts:
            try:
                idx = user_opts.index(opt)
                user_opt = user_opts[idx]
                res.extend(user_opt.get_list())
                del user_opts[idx]
            except ValueError:
                res.extend(opt.get_list())
        for opt in user_opts:
            res.extend(opt.get_list())
        return res

    def convert(
        self,
            input_file: str | Path,
            output_file: str | Path,
            overwrite_output: bool = True,
            stats: bool = False,
            in_options: list[BackendOption] | None = None,
            out_options: list[BackendOption] | None = None,
            progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Execute the FFmpeg command to convert the input file to the output file.

        :param input_file: Input file path.
        :param output_file: Output file path.      
        :param overwrite_output: Overwrite output file (no user confirmation prompt). Defaults to True.      
        :param stats: Show progress stats. Defaults to False.      
        :param in_options: Additional input options. Defaults to None.      
        :param out_options: Additional output options. Defaults to None.    
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :return: Subprocess.Popen object

        :raises RuntimeError: If FFmpeg encounters an error during execution.
        """
        # set input/output files and options
        in_def_opts = self._get_input_defaults(input_file)
        out_def_opts = self._get_output_defaults(output_file)

        in_opts = self._override_with(in_def_opts, in_options if in_options else [])
        out_opts = self._override_with(out_def_opts, out_options if out_options else [])

        # set global options
        global_options = [
            # overwrite output (no confirm)
            "-y" if overwrite_output else "-n",
            "-v" if self._verbose else "",  # verbose output
            "-stats" if stats else "",  # print progress stats
        ]

        # build ffmpeg command
        ffmpeg_command = []
        ffmpeg_command.extend([str(self._ffmpeg_bin)])  # ffmpeg CLI
        ffmpeg_command.extend(global_options)    # set global options
        ffmpeg_command.extend(in_opts)           # set in options
        ffmpeg_command.extend(["-i", str(input_file)])   # set input
        ffmpeg_command.extend(out_opts)          # set out options
        ffmpeg_command.extend([str(output_file)])        # set output

        # remove empty strings
        ffmpeg_command = [arg for arg in ffmpeg_command if arg != ""]

        # Execute the FFmpeg command
        process = Environment.run_nowait(
            *ffmpeg_command,
        )

        file_duration_secs = self.calculate_file_total_duration(input_file)
        while process.poll() is None:
            if not process.stdout:
                continue

            match = FFmpegBackend.PROGRESS_RE.search(process.stdout.readline())
            if not match:
                continue
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3))

            current_time = hours * 3600 + minutes * 60 + seconds
            progress = 100.0 * (float(current_time) / file_duration_secs)
            if progress_callback:
                progress_callback(progress)

        Environment.check_returncode(process)
        return process
