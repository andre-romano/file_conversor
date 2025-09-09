# src\file_conversor\backend\audio_video\ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

import subprocess
import json
import re

from pathlib import Path
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.backend.audio_video.format_container import AudioCodec, VideoCodec, FormatContainer, AVAILABLE_VIDEO_CONTAINERS, AVAILABLE_AUDIO_CONTAINERS
from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_file_format

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager

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

    SUPPORTED_OUT_AUDIO_FORMATS = AVAILABLE_AUDIO_CONTAINERS
    SUPPORTED_OUT_VIDEO_FORMATS = AVAILABLE_VIDEO_CONTAINERS
    SUPPORTED_OUT_FORMATS = SUPPORTED_OUT_VIDEO_FORMATS | SUPPORTED_OUT_AUDIO_FORMATS

    PROGRESS_RE = re.compile(r'time=(\d+):(\d+):([\d\.]+)')

    EXTERNAL_DEPENDENCIES = set([
        "ffmpeg",
        "ffprobe",
    ])

    @classmethod
    def __get_supported_codecs(cls, supported_format: dict[str, FormatContainer], is_audio: bool, ext: str | None = None) -> Iterable[str]:
        res: set[str] = set()
        for cont_ext, container in supported_format.items():
            if not ext or (ext == cont_ext):
                res.update([str(c) for c in (container.available_audio_codecs if is_audio else container.available_video_codecs)])
        return sorted(res)

    @classmethod
    def get_supported_audio_codecs(cls, ext: str | None = None) -> Iterable[str]:
        return cls.__get_supported_codecs(cls.SUPPORTED_OUT_AUDIO_FORMATS, is_audio=True, ext=ext)

    @classmethod
    def get_supported_video_codecs(cls, ext: str | None = None) -> Iterable[str]:
        return cls.__get_supported_codecs(cls.SUPPORTED_OUT_VIDEO_FORMATS, is_audio=False, ext=ext)

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

    def _get_input_options(self, input_file: str | Path) -> list[str]:
        """
        Set the input file and check if it has a supported format.

        :param input_file: Input file path.

        :return:  in options

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        res: list[str] = []
        # check file is found
        input_path = Path(input_file)
        if not input_path.exists() and not input_path.is_file():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # check if the input file has a supported format
        check_file_format(input_path, self.SUPPORTED_IN_FORMATS)

        # set the input format options based on the file extension
        in_ext = input_path.suffix[1:]
        for k, v in self.SUPPORTED_IN_FORMATS[in_ext].items():
            res.extend([str(k), str(v)])
        return res

    def _get_output_options(
            self,
            output_file: str | Path,
            audio_bitrate: int | None = None,
            video_bitrate: int | None = None,
            audio_codec: str | None = None,
            video_codec: str | None = None,
            width: int | None = None,
            height: int | None = None,
            fps: int | None = None,
            rotate: int | None = None,
            mirror_axis: str | None = None,
    ) -> list[str]:
        """
        Set the output file and check if it has a supported format.

        :param output_file: Output file path.
        :param audio_bitrate: Audio bitrate to use. Defaults to None (use source bitrate).      
        :param video_bitrate: Video bitrate to use. Defaults to None (use source bitrate).      
        :param audio_codec: Audio codec to use. Defaults to None (use container default codec).      
        :param video_codec: Video codec to use. Defaults to None (use container default codec).      
        :param width: Target width (in pixels). Defaults to None (use the same as source).      
        :param height: Target height (in pixels). Defaults to None (use the same as source).      
        :param fps: Video FPS. Defaults to None (use the same as source).      
        :param rotate: Rotate video (clockwise). Defaults to None (do not rotate).      
        :param mirror_axis: Mirror axis. Valid options are: x, y. Defaults to None (do not mirror).      

        :return: out options

        :raises typer.BadParameter: Unsupported format, or file not found.
        """
        # create out dir (if it does not exists)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # check if the output file has a supported format
        check_file_format(output_path, self.SUPPORTED_OUT_FORMATS)

        # set the output format options based on the file extension
        out_ext = output_path.suffix[1:]
        container = self.SUPPORTED_OUT_FORMATS[out_ext]

        # audio codec
        if audio_codec:
            container.audio_codec = AudioCodec.from_str(audio_codec)

        if audio_bitrate:
            container.audio_codec.set_bitrate(audio_bitrate)

        # video codec
        if video_codec:
            container.video_codec = VideoCodec.from_str(video_codec)

        if video_bitrate:
            container.video_codec.set_bitrate(video_bitrate)

        if fps:
            container.video_codec.set_fps(fps)

        if width and height:
            container.video_codec.set_resolution(width=width, height=height)
        elif (width and not height) or (not width and height):
            raise ValueError(f"{_('Invalid width or height')} '{width} x {height}'. {_('Video resizer requires both options to work')}.")

        if rotate:
            container.video_codec.set_rotation(rotate)

        if mirror_axis:
            container.video_codec.set_mirror(mirror_axis)

        # get options
        return container.get_options()

    def _get_resolution(self, file_path: str | Path):
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

    def _execute_progress_callback(
        self,
        input_file: str | Path,
        process: subprocess.Popen,
        progress_callback: Callable[[float], Any] | None = None,
    ):
        file_duration_secs = self._calculate_file_total_duration(input_file)
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

    def _calculate_file_total_duration(self, file_path: str | Path) -> float:
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

    def info(self, file_path: str | Path) -> dict:
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

    def check(
        self,
        file_path: str | Path,
        progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Check file integrity

        :raises subprocess.CalledProcessError: if file is corrupted
        """
        try:
            process = Environment.run_nowait(
                f"{self._ffmpeg_bin}",
                "-v", "error",
                "-i", str(file_path),
                "-f", "null", "-"
            )
            self._execute_progress_callback(
                input_file=file_path,
                process=process,
                progress_callback=progress_callback,
            )
            logger.info(rf"'{file_path}': [bold green]OK[/]")
        except subprocess.CalledProcessError as e:
            logger.error(rf"'{file_path}': [bold red]FAILED[/]")
            raise

    def convert(
        self,
            input_file: str | Path,
            output_file: str | Path,
            audio_bitrate: int | None = None,
            video_bitrate: int | None = None,
            audio_codec: str | None = None,
            video_codec: str | None = None,
            width: int | None = None,
            height: int | None = None,
            fps: int | None = None,
            rotate: int | None = None,
            mirror_axis: str | None = None,
            overwrite_output: bool = True,
            stats: bool = False,
            progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Execute the FFmpeg command to convert the input file to the output file.

        :param input_file: Input file path.
        :param output_file: Output file path.      
        :param audio_bitrate: Audio bitrate to use. Defaults to None (use source bitrate).      
        :param video_bitrate: Video bitrate to use. Defaults to None (use source bitrate).      
        :param audio_codec: Audio codec to use. Defaults to None (use container default codec).      
        :param video_codec: Video codec to use. Defaults to None (use container default codec).      
        :param width: Target width (in pixels). Defaults to None (use the same as source).      
        :param height: Target height (in pixels). Defaults to None (use the same as source).      
        :param fps: Video FPS. Defaults to None (use the same as source).      
        :param rotate: Rotate video (clockwise). Defaults to None (do not rotate).      
        :param mirror_axis: Mirror axis. Valid options are: x, y. Defaults to None (do not mirror).      
        :param overwrite_output: Overwrite output file (no user confirmation prompt). Defaults to True.      
        :param stats: Show progress stats. Defaults to False.      
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :return: Subprocess.Popen object

        :raises RuntimeError: If FFmpeg encounters an error during execution.
        """
        # set input/output files and options
        in_opts = self._get_input_options(input_file)

        out_opts = self._get_output_options(
            output_file,
            audio_bitrate=audio_bitrate,
            video_bitrate=video_bitrate,
            audio_codec=audio_codec,
            video_codec=video_codec,
            width=width,
            height=height,
            fps=fps,
            rotate=rotate,
            mirror_axis=mirror_axis,
        )

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

        self._execute_progress_callback(
            input_file=input_file,
            process=process,
            progress_callback=progress_callback,
        )

        Environment.check_returncode(process)
        return process
