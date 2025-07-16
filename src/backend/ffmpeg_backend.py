# src/backend/ffmpeg_backend.py

"""
This module provides functionalities for handling audio and video files using FFmpeg.
"""

from backend.backend_abstract import BackendAbstract
from utils.file import File

import imageio_ffmpeg
import ffmpeg
import os

FFMPEG_BINARY = None


class FFmpegBackend(BackendAbstract):
    """
    FFmpegBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    It inherits from BackendAbstract and implements methods to set input and output files.
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
            'format': 'mp3',
            'acodec': 'libmp3lame',
            'audio_bitrate': '192k',
        },
        'm4a': {
            'format': 'ipod',
            'acodec': 'aac',
            'audio_bitrate': '192k',
        },
        'ogg': {
            'format': 'ogg',
            'acodec': 'libvorbis',
            'audio_bitrate': '192k',
        },
        'opus': {
            'format': 'opus',
            'acodec': 'libopus',
            'audio_bitrate': '192k',
        },
        'flac': {
            'format': 'flac',
            'acodec': 'flac',
        },
    }
    SUPPORTED_OUT_VIDEO_FORMATS = {
        'mp4': {
            'format': 'mp4',
            'vcodec': 'libx264',
            'acodec': 'aac',
            'audio_bitrate': '192k',
        },
        'avi': {
            'format': 'avi',
            'vcodec': 'mpeg4',
            'acodec': 'libmp3lame',
            'audio_bitrate': '192k',
        },
        'mkv': {
            'format': 'matroska',
            'vcodec': 'libx264',
            'acodec': 'aac',
            'audio_bitrate': '192k',
        },
        'webm': {
            'format': 'webm',
            'vcodec': 'libvpx',
            'acodec': 'libvorbis',
            'audio_bitrate': '192k',
        },
    }
    SUPPORTED_OUT_FORMATS = SUPPORTED_OUT_VIDEO_FORMATS | SUPPORTED_OUT_AUDIO_FORMATS

    def __init__(self, input_file: str, output_file: str, **kwargs):
        super().__init__(input_file, output_file, **kwargs)

        # Get the FFmpeg binary path
        FFMPEG_BINARY = imageio_ffmpeg.get_ffmpeg_exe()
        os.environ["FFMPEG_BINARY"] = FFMPEG_BINARY
        print("FFmpeg path:", FFMPEG_BINARY)

    def _set_input(self, input_file: str):
        """
        Set the input file and check if it has a supported format.
        :param input_file: Input file path.

        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the input file format is not supported.
        """
        super()._set_input(input_file)
        in_file = File(input_file)

        # check if the input file has a supported format
        in_file.check_supported_format(self.SUPPORTED_IN_FORMATS)

        # set the input format options based on the file extension
        in_ext = in_file.get_extension()
        self.options.update(self.SUPPORTED_IN_FORMATS[in_ext])

    def _set_output(self, output_file: str):
        """
        Set the output file and check if it has a supported format.
        :param output_file: Output file path.

        :raises FileNotFoundError: If the output directory could not be created.
        :raises ValueError: If the output file format is not supported.
        :return: self (FFmpegBackend instance)
        """
        super()._set_output(output_file)
        out_file = File(output_file)

        # check if the output file has a supported format
        File(output_file).check_supported_format(self.SUPPORTED_OUT_FORMATS)

        # set the output format options based on the file extension
        out_ext = out_file.get_extension()
        self.options.update(self.SUPPORTED_OUT_FORMATS[out_ext])

    def execute(self) -> tuple[str, str]:
        """
        Execute the FFmpeg command to convert the input file to the output file.

        :return: A tuple containing the standard output and error messages.

        :raises RuntimeError: If FFmpeg encounters an error during execution.
        """

        print(f"Executing FFmpeg command:")
        print(f" IN: {self.input_file}")
        print(f"OUT: {self.output_file}")
        print(f"OPT: {self.options}")

        # Execute the FFmpeg command
        out, err = ffmpeg.input(self.input_file).output(
            self.output_file,
            **self.options
        ).run(
            cmd=FFMPEG_BINARY,
            capture_stdout=True,
            capture_stderr=True
        )

        # Verificar mensagens de erro no stderr
        stdout_text = out.decode('utf-8').lower()
        stderr_text = err.decode('utf-8').lower()
        if "error" in stderr_text:
            raise RuntimeError(f"FFmpeg error: {stderr_text}")
        else:
            return stdout_text, stderr_text
