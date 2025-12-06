# src\file_conversor\backend\audio_video\ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

import subprocess
import re

from pathlib import Path
from typing import Any, Callable, Iterable

from cv2 import log

# user-provided imports
from file_conversor.backend.audio_video.abstract_ffmpeg_backend import AbstractFFmpegBackend
from file_conversor.backend.audio_video.ffprobe_backend import FFprobeBackend

from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter
from file_conversor.backend.audio_video.ffmpeg_codec import FFmpegAudioCodec, FFmpegVideoCodec
from file_conversor.backend.audio_video.format_container import FormatContainer

from file_conversor.config import Environment, Log, get_translation

from file_conversor.utils.validators import check_file_format
from file_conversor.utils.command_manager import CommandManager

from file_conversor.system import is_windows

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegBackend(AbstractFFmpegBackend):
    """
    FFmpegBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    """

    EXTERNAL_DEPENDENCIES: set[str] = {
        "ffmpeg",
    }

    @staticmethod
    def _clean_two_pass_log_file(logfile: Path | None):
        if logfile is None:
            return
        for filepath in logfile.parent.glob(logfile.name + "-0.log*"):
            try:
                if not filepath.exists():
                    continue
                filepath.unlink()
            except Exception as e:
                logger.warning(f"Failed to remove log file '{filepath}': {e}")

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

        self._global_options: list[str] = [
            "" if not verbose else "-v",
            "" if not stats else "-stats",
            "-n" if not overwrite_output else "-y",
        ]
        self._in_opts: list[str] = []
        self._out_opts: list[str] = []

        self._out_container: FormatContainer | None = None

        self._input_file: Path | None = None
        self._output_file: Path | None = None
        self._pass_logfile: Path | None = None

        self._audio_bitrate: int | None = None
        self._video_bitrate: int | None = None

        self._progress_callback: Callable[[float], Any] | None = None

    def _execute_progress_callback(
        self,
        process: subprocess.Popen,
    ):
        """returns output lines read"""
        lines: list[str] = []
        PROGRESS_RE = re.compile(r'time=(\d+):(\d+):([\d\.]+)')

        ffprobe_backend = FFprobeBackend(install_deps=self._install_deps, verbose=self._verbose)
        if not self._input_file:
            raise RuntimeError(f"{_('Input file not set')}")

        file_duration_secs = ffprobe_backend.get_duration(self._input_file)
        while process.poll() is None:
            if not process.stdout:
                continue

            line = process.stdout.readline()
            match = PROGRESS_RE.search(line)
            if not match:
                lines.append(line)
                continue
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3))

            current_time = hours * 3600 + minutes * 60 + seconds
            progress = 100.0 * (float(current_time) / file_duration_secs)
            if self._progress_callback:
                self._progress_callback(progress)
        return lines

    def _set_input_file(self, input_file: str | Path):
        """
        Set the input file and check if it has a supported format.

        :param input_file: Input file path.

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        self._in_opts = []

        # check file is found
        self._input_file = Path(input_file).resolve()
        if not self._input_file.exists() and not self._input_file.is_file():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # check if the input file has a supported format
        check_file_format(self._input_file, self.SUPPORTED_IN_FORMATS)

        # set the input format options based on the file extension
        in_ext = self._input_file.suffix[1:].lower()
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
        self._output_file = Path(output_file).resolve()
        self._output_file = self._output_file.with_suffix(self._output_file.suffix.lower())

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
        self._set_pass_logfile()

    def _set_pass_logfile(self):
        if not self._output_file:
            raise RuntimeError(f"{_('Output file not set')}")

        logdir = self._output_file.parent
        self._pass_logfile = logdir / CommandManager.get_output_file(self._output_file, stem="-ffmpeg2pass", suffix="")
        logger.debug(f"{_('Temporary 2-pass log file')}: {self._pass_logfile}")

    def set_files(self, input_file: str | Path, output_file: str | Path):
        """
        Set input/output files, and default global options

        :param input_file: Input file path.
        :param output_file: Output file path.      
        """
        self._set_input_file(input_file)
        self._set_output_file(output_file)

    def _set_codec(
            self,
            is_audio: bool,
            codec: str | None = None,
            bitrate: int | None = None,
            filters: FFmpegFilter | Iterable[FFmpegFilter] | None = None,
    ):
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")

        if codec:
            if is_audio:
                self._out_container.audio_codec = FFmpegAudioCodec.from_str(codec)
            else:
                self._out_container.video_codec = FFmpegVideoCodec.from_str(codec)

        codec_obj = self._out_container.audio_codec if is_audio else self._out_container.video_codec

        if bitrate is not None and bitrate > 0:
            if is_audio:
                self._audio_bitrate = bitrate
            else:
                self._video_bitrate = bitrate
            codec_obj.set_bitrate(bitrate)

        if filters:
            if isinstance(filters, FFmpegFilter):
                filters = [filters]
            codec_obj.set_filters(*filters)

    def set_audio_codec(
        self,
        codec: str | None = None,
        bitrate: int | None = None,
        filters: FFmpegFilter | Iterable[FFmpegFilter] | None = None,
    ):
        """
        Set audio codec and bitrate

        :param codec: Codec to use. Defaults to None (use container default codec).      
        :param bitrate: Bitrate to use (in kbps). Defaults to None (use FFmpeg defaults).      
        :param filters: Filters to use. Defaults to None (do not use any filter).      

        :raises RuntimeErrors: if output container not set
        """
        self._set_codec(is_audio=True, codec=codec, bitrate=bitrate, filters=filters)

    def set_video_codec(
        self,
        codec: str | None = None,
        bitrate: int | None = None,
        filters: FFmpegFilter | Iterable[FFmpegFilter] | None = None,
        encoding_speed: str | None = None,
        quality_setting: str | None = None,
    ):
        """
        Seet video codec and bitrate

        :param codec: Codec to use. Defaults to None (use container default codec).      
        :param bitrate: Bitrate to use (in kbps). Defaults to None (use FFmpeg defaults).      
        :param filters: Filters to use. Defaults to None (do not use any filter).      
        :param encoding_speed: Encoding speed to use. Defaults to None (use codec default speed).      
        :param quality_setting: Quality setting to use. Defaults to None (use codec default quality).

        :raises RuntimeErrors: if output container not set
        """
        self._set_codec(is_audio=False, codec=codec, bitrate=bitrate, filters=filters)
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")

        if encoding_speed:
            self._out_container.video_codec.set_encoding_speed(encoding_speed)

        if (not bitrate or bitrate == 0) and quality_setting:
            self._out_container.video_codec.set_quality_setting(quality_setting)

    def _get_two_pass_options(self, pass_num: int) -> list[str]:
        if pass_num <= 0:
            return []

        if self._audio_bitrate and self._audio_bitrate <= 0:
            raise ValueError(f"{_('Audio Bitrate cannot be 0 when using two-pass mode.')}")
        if self._video_bitrate and self._video_bitrate <= 0:
            raise ValueError(f"{_('Video Bitrate cannot be 0 when using two-pass mode.')}")
        if not self._pass_logfile:
            raise RuntimeError(f"{_('2-pass log file not set')}")

        # add 2-pass encoding options
        return [
            "-pass", str(pass_num),
            "-passlogfile", str(self._pass_logfile),
        ]

    def _execute(self):
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

        out_lines = self._execute_progress_callback(
            process=process,
        )

        Environment.check_returncode(process, out_lines=out_lines)
        return process

    def execute(
        self,
        progress_callback: Callable[[float], Any] | None = None,
        pass_num: int = 0,
        out_opts: list[str] | None = None,
    ):
        """
        Execute the FFmpeg command to convert the input file to the output file.

        :param pass_num: Pass number for multi-pass encoding (0 for single pass, 1 for first pass, 2 for second pass). Defaults to 0.
        :param out_opts: FFmpeg custom out options. Defaults to None.

        :return: Subprocess.Popen object

        :raises RuntimeError: If FFmpeg encounters an error during execution.
        """
        self._progress_callback = progress_callback

        if pass_num not in (0, 1, 2):
            raise ValueError(f"{_('Invalid number of passes:')} {pass_num}. {_('Must be 0 (single-pass), 1 (first pass) or 2 (second pass).')}")

        if not self._input_file or not self._output_file:
            raise RuntimeError(f"{_('Input/output files not set')}")

        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")

        self._out_opts = [
            *self._get_two_pass_options(pass_num),
            *self._out_container.get_options(),
            *(out_opts or []),
        ]

        original_output_file = self._output_file
        if pass_num == 1:
            self._output_file = Path("NUL" if is_windows() else "/dev/null")

        try:
            self._execute()
        except:
            self._clean_two_pass_log_file(self._pass_logfile)
            raise

        self._output_file = original_output_file

        if pass_num in (0, 2):
            self._clean_two_pass_log_file(self._pass_logfile)


__all__ = [
    "FFmpegBackend",
]
