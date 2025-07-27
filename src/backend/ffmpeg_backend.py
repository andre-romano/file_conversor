# src/backend/ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

import json
import os
import shutil
import subprocess
import re

from datetime import timedelta
from typing import Iterable

# user-provided imports
from utils import File

from dependency import BrewPackageManager, ScoopPackageManager
from backend.abstract_backend import AbstractBackend


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
            '-f': 'mp3',
            '-c:a': 'libmp3lame',
        },
        'm4a': {
            '-f': 'ipod',
            '-c:a': 'aac',
        },
        'ogg': {
            '-f': 'ogg',
            '-c:a': 'libvorbis',
        },
        'opus': {
            '-f': 'opus',
            '-c:a': 'libopus',
        },
        'flac': {
            '-f': 'flac',
            '-c:a': 'flac',
        },
    }
    SUPPORTED_OUT_VIDEO_FORMATS = {
        'mp4': {
            '-f': 'mp4',
            '-c:v': 'libx264',
            '-c:a': 'aac',
        },
        'avi': {
            '-f': 'avi',
            '-c:v': 'mpeg4',
            '-c:a': 'libmp3lame',
        },
        'mkv': {
            '-f': 'matroska',
            '-c:v': 'libx264',
            '-c:a': 'aac',
        },
        'webm': {
            '-f': 'webm',
            '-c:v': 'libvpx',
            '-c:a': 'libvorbis',
        },
    }
    SUPPORTED_OUT_FORMATS = SUPPORTED_OUT_VIDEO_FORMATS | SUPPORTED_OUT_AUDIO_FORMATS

    PROGRESS_RE = re.compile(r'time=(\d+):(\d+):([\d\.]+)')

    @staticmethod
    def get_convert_progress(process: subprocess.Popen, file_duration_secs: float) -> float:
        """
        Gets FFMpeg current progress status, in percentage (0-100)

        :param process: Subprocess.Popen object.
        :param file_duration_secs: Input file duration (in secs).

        :return: Progress of FFMpeg [0-100], otherwise 0
        """
        if process and process.stderr:
            match = FFmpegBackend.PROGRESS_RE.search(process.stderr.readline())
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                seconds = float(match.group(3))
                current_time = hours * 3600 + minutes * 60 + seconds
                return 100.0 * (float(current_time) / file_duration_secs)
        return 0

    def __init__(
        self,
        install_deps: bool | None = None
    ):
        """
        Initialize the FFMpeg backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. Defaults to None.      

        :raises FileNotFoundError: If the input file does not exist, or output directory could not be created.
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

        ffprobe_bin = shutil.which("ffprobe")
        self._ffprobe_bin = ffprobe_bin if ffprobe_bin else "FFPROBE_NOT_FOUND"

        ffmpeg_bin = shutil.which("ffmpeg")
        self._ffmpeg_bin = ffmpeg_bin if ffmpeg_bin else "FFMPEG_NOT_FOUND"

    def calculate_file_total_duration(self, file_path: str) -> float:
        """
        Calculate file total duration (in secs), using `ffprobe`.

        :return: Total duration in seconds.
        """
        result = subprocess.run(
            [self._ffprobe_bin, '-v', 'error', '-show_entries',
             'format=duration', '-of',
             'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        duration_str = result.stdout.strip()
        return float(duration_str if duration_str else "0")

    def calculate_file_formatted_duration(self, file_path: str) -> str:
        """
        Calculate file duration (formatted), using `ffprobe`.

        :return: Total duration  (format HH:MM:SS).
        """
        duration_secs = self.calculate_file_total_duration(file_path)

        # Converte segundos para timedelta e formata como HH:MM:SS
        td = timedelta(seconds=int(duration_secs))
        return str(td)

    def get_file_info(self, file_path: str) -> dict:
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
        command = [
            self._ffprobe_bin,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            "-show_error",
            file_path
        ]
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return json.loads(result.stdout)

    def _set_input(self, input_file: str) -> tuple[str, list]:
        """
        Set the input file and check if it has a supported format.

        :param input_file: Input file path.

        :return: (Input file, in options).

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        # check file is found
        in_file = File(input_file)
        if not in_file.is_file():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # check if the input file has a supported format
        in_file.check_supported_format(self.SUPPORTED_IN_FORMATS)

        # set the input format options based on the file extension
        in_opts = []
        in_ext = in_file.get_extension()
        for opt, value in self.SUPPORTED_IN_FORMATS[in_ext].items():
            in_opts.extend([opt, value])

        return input_file, in_opts

    def _set_output(self, output_file: str) -> tuple[str, list]:
        """
        Set the output file and check if it has a supported format.

        :param output_file: Output file path.

        :return: (Output file, out options).

        :raises FileExistsError: If the output path is a file.
        :raises FileNotFoundError: If the output directory could not be created.
        :raises ValueError: If the output file format is not supported.        
        """
        out_file = File(output_file)

        # create out dir (if it does not exists)
        out_dir = File(out_file.get_full_dirname())
        out_dir.create_dir()

        # check if the output file has a supported format
        File(output_file).check_supported_format(self.SUPPORTED_OUT_FORMATS)

        # set the output format options based on the file extension
        out_opts = []
        out_ext = out_file.get_extension()
        for opt, value in self.SUPPORTED_OUT_FORMATS[out_ext].items():
            out_opts.extend([opt, value])

        return output_file, out_opts

    def convert(
        self,
            input_file: str,
            output_file: str,
            overwrite_output: bool = True,
            stats: bool = False,
        verbose: bool = False,
            in_options: Iterable | None = None,
            out_options: Iterable | None = None,
    ) -> subprocess.Popen:
        """
        Execute the FFmpeg command to convert the input file to the output file.

        :param input_file: Input file path.
        :param output_file: Output file path.      
        :param overwrite_output: Overwrite output file (no user confirmation prompt). Defaults to True.      
        :param stats: Show progress stats. Defaults to False.      
        :param verbose: Verbose logging. Defaults to False.      
        :param in_options: Additional input options. Defaults to None.      
        :param out_options: Additional output options. Defaults to None.    

        :return: Subprocess.Popen object

        :raises RuntimeError: If FFmpeg encounters an error during execution.
        """
        # set input/output files and options
        in_file, in_opts = self._set_input(input_file)
        out_file, out_opts = self._set_output(output_file)

        in_opts.extend(in_options if in_options else [])
        out_opts.extend(out_options if out_options else [])

        # set global options
        global_options = [
            # overwrite output (no confirm)
            "-y" if overwrite_output else "-n",
            "-v" if verbose else "",  # verbose output
            "-stats" if stats else "",  # print progress stats
        ]

        # build ffmpeg command
        ffmpeg_command = []
        ffmpeg_command.extend([self._ffmpeg_bin])  # ffmpeg CLI
        ffmpeg_command.extend(global_options)    # set global options
        ffmpeg_command.extend(in_opts)           # set in options
        ffmpeg_command.extend(["-i", in_file])   # set input
        ffmpeg_command.extend(out_opts)          # set out options
        ffmpeg_command.extend([out_file])        # set output

        # remove empty strings
        ffmpeg_command = [arg for arg in ffmpeg_command if arg != ""]

        print(f"--------------------")
        print(f"Executing FFmpeg:")
        print(f" IN: {in_file}")
        print(f"OUT: {out_file}")
        print(f"OPT: {in_opts}")
        print(f" ")
        print(f"{" ".join(ffmpeg_command)}")
        print(f"--------------------")

        # Execute the FFmpeg command
        _convert_process = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return _convert_process
