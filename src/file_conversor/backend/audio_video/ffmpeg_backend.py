# src\file_conversor\backend\audio_video\ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

import subprocess

from pathlib import Path
from typing import Any, Callable

# user-provided imports
from file_conversor.backend.audio_video.abstract_ffmpeg_backend import (
    AbstractFFmpegBackend,
)
from file_conversor.backend.audio_video.codec import (
    FFmpegAudioCodecs,
    FFmpegVideoCodec,
    FFmpegVideoCodecs,
)
from file_conversor.backend.audio_video.container.format_container import (
    FormatContainer,
)
from file_conversor.backend.audio_video.ffprobe_backend import FFprobeBackend
from file_conversor.backend.audio_video.filter.ffmpeg_filter import FFmpegFilter
from file_conversor.config import Environment, Log, get_translation
from file_conversor.system import System
from file_conversor.utils.formatters import get_output_file


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

    VideoProfile = FFmpegVideoCodec.ProfileSetting
    VideoQuality = FFmpegVideoCodec.QualitySetting
    VideoEncoding = FFmpegVideoCodec.EncodingSetting

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

    @staticmethod
    def build_filter(name: str) -> FFmpegFilter:
        """ Build FFmpegFilter from string name. """
        return FFmpegFilter.from_str(name)

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
            "-n" if not overwrite_output else "-y",
            "" if not stats else "-stats",
        ]
        self._in_opts: list[str] = []
        self._out_opts: list[str] = []

        self._out_container: FormatContainer | None = None

        self._input_file: Path | None = None
        self._output_file: Path | None = None
        self._pass_logfile: Path | None = None

        self._audio_bitrate: int = -1
        self._video_bitrate: int = -1

        self._progress_callback: Callable[[float], Any] | None = None

    def _execute_progress_callback(
        self,
        process: subprocess.Popen[Any],
    ):
        """returns output lines read"""
        import re

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

    def _set_input_file(self, input_file: Path):
        """
        Set the input file and check if it has a supported format.

        :param input_file: Input file path.

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        self._in_opts = []

        self._input_file = input_file.resolve()

    def _set_output_file(
            self,
            output_file: Path,
    ):
        """
        Set the output file and check if it has a supported format.

        :param output_file: Output file path.

        :raises typer.BadParameter: Unsupported format.
        """
        self._out_opts = []

        self._output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext: str = ""
        if self._output_file.name == "-":
            logger.warning("Null container selected. No output file will be created.")
            out_ext = "null"
        else:
            self._output_file.parent.mkdir(parents=True, exist_ok=True)

            # set the output format options based on the file extension
            out_ext = self._output_file.suffix[1:]

        if out_ext in self.SupportedOutAudioFormats:
            self._out_container = self.SupportedOutAudioFormats(out_ext).container
        elif out_ext in self.SupportedOutVideoFormats:
            self._out_container = self.SupportedOutVideoFormats(out_ext).container
        else:
            raise ValueError(f"{_('Unsupported output format:')} {out_ext}")
        self._set_pass_logfile()

    def _set_pass_logfile(self):
        if not self._output_file:
            raise RuntimeError(f"{_('Output file not set')}")

        logdir = self._output_file.parent
        self._pass_logfile = get_output_file(
            output_dir=logdir,
            input_file=self._output_file,
            out_stem="-ffmpeg2pass",
            out_suffix="",
        )
        logger.debug(f"{_('Temporary 2-pass log file')}: {self._pass_logfile}")

    def set_files(self, input_file: Path, output_file: Path):
        """
        Set input/output files, and default global options

        :param input_file: Input file path.
        :param output_file: Output file path.      
        """
        self._set_input_file(input_file)
        self._set_output_file(output_file)

    def set_audio_codec(
        self,
        *filters: FFmpegFilter,
        codec: FFmpegAudioCodecs | None = None,
        bitrate: int | None = None,
    ):
        """
        Set audio codec and bitrate

        :param codec: Codec to use. Defaults to None (use container default codec).      
        :param bitrate: Bitrate to use (in kbps). Defaults to -1 (use FFmpeg defaults).      
        :param filters: Filters to use. Defaults to None (do not use any filter).      

        :raises RuntimeErrors: if output container not set
        """
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")

        if codec:
            self._out_container.audio_codec = codec.codec

        audio_codec = self._out_container.audio_codec
        audio_codec.set_filters(*filters)

        if bitrate is not None:
            audio_codec.set_bitrate(bitrate)

    def set_video_codec(
        self,
        *filters: FFmpegFilter,
        codec: FFmpegVideoCodecs | None = None,
        bitrate: int | None = None,
        profile_setting: VideoProfile | None = None,
        encoding_speed: VideoEncoding | None = None,
        quality_setting: VideoQuality | None = None,
    ):
        """
        Seet video codec and bitrate

        :param codec: Codec to use. Defaults to None (use container default codec).      
        :param bitrate: Bitrate to use (in kbps). Defaults to -1 (use FFmpeg defaults).      
        :param filters: Filters to use. Defaults to None (do not use any filter).      
        :param encoding_speed: Encoding speed to use. Defaults to None (use codec default speed).      
        :param quality_setting: Quality setting to use. Defaults to None (use codec default quality).

        :raises RuntimeErrors: if output container not set
        """
        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")

        if codec:
            self._out_container.video_codec = codec.codec

        video_codec = self._out_container.video_codec
        video_codec.set_filters(*filters)

        if bitrate is not None:
            video_codec.set_bitrate(bitrate)

        if profile_setting != None:
            video_codec.set_profile(profile_setting)

        if encoding_speed != None:
            video_codec.set_encoding_speed(encoding_speed)

        if quality_setting != None:
            video_codec.set_quality_setting(quality_setting)

    def _get_two_pass_options(self, pass_num: int) -> list[str]:
        if pass_num <= 0:
            return []

        if not self._out_container:
            raise RuntimeError(f"{_('Output container not set')}")

        audio_codec = self._out_container.audio_codec
        video_codec = self._out_container.video_codec

        if audio_codec.bitrate <= 0:
            raise ValueError(f"{_('Audio Bitrate cannot be 0 when using two-pass mode.')}")

        if video_codec.bitrate <= 0:
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
        ffmpeg_command: list[str] = []
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
            self._output_file = Path("/dev/null")
            if System.Platform.get() == System.Platform.WINDOWS:
                self._output_file = Path("NUL")

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
