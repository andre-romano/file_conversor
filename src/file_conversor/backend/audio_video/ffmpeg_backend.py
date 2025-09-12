# src\file_conversor\backend\audio_video\ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

import subprocess
import re

from pathlib import Path
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.backend.audio_video.abstract_ffmpeg_backend import AbstractFFmpegBackend
from file_conversor.backend.audio_video.ffprobe_backend import FFprobeBackend

from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter
from file_conversor.backend.audio_video.ffmpeg_codec import FFmpegAudioCodec, FFmpegVideoCodec
from file_conversor.backend.audio_video.format_container import FormatContainer

from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_file_format

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegBackend(AbstractFFmpegBackend):
    """
    FFmpegBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    """

    EXTERNAL_DEPENDENCIES = set([
        "ffmpeg",
    ])

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
        overwrite_output: bool = False,
        stats: bool = False,
    ):
        """
        Initialize the FFMpeg backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 
        :param verbose: Verbose logging. Defaults to False.      

        :raises RuntimeError: if ffmpeg dependency is not found
        """
        super().__init__(
            install_deps=install_deps,
            verbose=verbose,
        )
        self._stats = stats
        self._overwrite_output = overwrite_output

        self._input_file: Path | None = None
        self._output_file: Path | None = None

        self._global_options: list[str] = []
        self._in_opts: list[str] = []
        self._out_opts: list[str] = []

        self._out_container: FormatContainer | None = None

    def _execute_progress_callback(
        self,
        process: subprocess.Popen,
        progress_callback: Callable[[float], Any] | None = None,
    ):
        PROGRESS_RE = re.compile(r'time=(\d+):(\d+):([\d\.]+)')

        ffprobe_backend = FFprobeBackend(install_deps=self._install_deps, verbose=self._verbose)
        if not self._input_file:
            raise RuntimeError(f"{_('Input file not set')}")

        file_duration_secs = ffprobe_backend.get_duration(self._input_file)
        while process.poll() is None:
            if not process.stdout:
                continue

            match = PROGRESS_RE.search(process.stdout.readline())
            if not match:
                continue
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3))

            current_time = hours * 3600 + minutes * 60 + seconds
            progress = 100.0 * (float(current_time) / file_duration_secs)
            if progress_callback:
                progress_callback(progress)

    def _set_global_options(self):
        """Set default global options"""
        global_options = {}
        global_options["-y" if self._overwrite_output else "-n"] = ""
        if self._verbose:
            global_options["-v"] = ""  # verbose output
        if self._stats:
            global_options["-stats"] = ""  # print progress stats

        # create global options list
        self._global_options = []
        for k, v in global_options.items():
            self._global_options.extend([str(k), str(v)])

    def _set_input_file(self, input_file: str | Path):
        """
        Set the input file and check if it has a supported format.

        :param input_file: Input file path.

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        self._in_opts = []

        # check file is found
        self._input_file = Path(input_file)
        if not self._input_file.exists() and not self._input_file.is_file():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # check if the input file has a supported format
        check_file_format(self._input_file, self.SUPPORTED_IN_FORMATS)

        # set the input format options based on the file extension
        in_ext = self._input_file.suffix[1:]
        for k, v in self.SUPPORTED_IN_FORMATS[in_ext].items():
            self._in_opts.extend([str(k), str(v)])

    def _set_output_file(
            self,
            output_file: str | Path,
    ):
        """
        Set the output file and check if it has a supported format.

        :param output_file: Output file path.

        :raises typer.BadParameter: Unsupported format.
        """
        self._out_opts = []

        # create out dir (if it does not exists)
        self._output_file = Path(output_file)
        if self._output_file.name == "-":
            logger.warning("Null container selected. No output file will be created.")
            out_ext = "null"
        else:
            self._output_file.parent.mkdir(parents=True, exist_ok=True)

            # check if the output file has a supported format
            check_file_format(self._output_file, self.SUPPORTED_OUT_FORMATS)

            # set the output format options based on the file extension
            out_ext = self._output_file.suffix[1:]
        args, kwargs = self.SUPPORTED_OUT_FORMATS[out_ext]
        self._out_container = FormatContainer(*args, **kwargs)

    def set_files(self, input_file: str | Path, output_file: str | Path):
        """
        Set input/output files, and default global options

        :param input_file: Input file path.
        :param output_file: Output file path.      
        """
        self._set_global_options()
        self._set_input_file(input_file)
        self._set_output_file(output_file)

    def set_audio_codec(self, codec: str | None = None, bitrate: int | None = None, filters: FFmpegFilter | Iterable[FFmpegFilter] | None = None):
        """
        Seet audio codec and bitrate

        :param codec: Codec to use. Defaults to None (use container default codec).      
        :param bitrate: Bitrate to use (in kbps). Defaults to None (use FFmpeg defaults).      
        :param filters: Filters to use. Defaults to None (do not use any filter).      

        :raises RuntimeErrors: if output container not set
        """
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")
        if codec:
            self._out_container.audio_codec = FFmpegAudioCodec.from_str(codec)
        if bitrate is not None and bitrate >= 0:
            self._out_container.audio_codec.set_bitrate(bitrate)
        if filters:
            if isinstance(filters, FFmpegFilter):
                filters = [filters]
            self._out_container.video_codec.set_filters(*filters)

    def set_video_codec(self, codec: str | None = None, bitrate: int | None = None, filters: FFmpegFilter | Iterable[FFmpegFilter] | None = None):
        """
        Seet video codec and bitrate

        :param codec: Codec to use. Defaults to None (use container default codec).      
        :param bitrate: Bitrate to use (in kbps). Defaults to None (use FFmpeg defaults).      

        :raises RuntimeErrors: if output container not set
        """
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")
        if codec:
            self._out_container.video_codec = FFmpegVideoCodec.from_str(codec)
        if bitrate is not None and bitrate >= 0:
            self._out_container.video_codec.set_bitrate(bitrate)
        if filters:
            if isinstance(filters, FFmpegFilter):
                filters = [filters]
            self._out_container.video_codec.set_filters(*filters)

    def execute(
        self,
        progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Execute the FFmpeg command to convert the input file to the output file.

        :return: Subprocess.Popen object

        :raises RuntimeError: If FFmpeg encounters an error during execution.
        """
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")
        self._out_opts = self._out_container.get_options()

        # build ffmpeg command
        ffmpeg_command = []
        ffmpeg_command.extend([str(self._ffmpeg_bin)])  # ffmpeg CLI
        ffmpeg_command.extend(self._global_options)    # set global options
        ffmpeg_command.extend(self._in_opts)           # set in options
        ffmpeg_command.extend(["-i", str(self._input_file)])   # set input
        ffmpeg_command.extend(self._out_opts)          # set out options
        ffmpeg_command.extend([str(self._output_file)])        # set output

        # remove empty strings
        ffmpeg_command = [arg for arg in ffmpeg_command if arg != ""]

        # Execute the FFmpeg command
        process = Environment.run_nowait(
            *ffmpeg_command,
        )

        self._execute_progress_callback(
            process=process,
            progress_callback=progress_callback,
        )

        Environment.check_returncode(process)
        return process
