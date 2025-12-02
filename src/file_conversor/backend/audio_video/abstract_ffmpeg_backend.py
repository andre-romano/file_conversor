# src\file_conversor\backend\audio_video\abstract_ffmpeg_backend.py


# user-provided imports
from typing import Any, Iterable
from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.backend.audio_video.format_container import AudioFormatContainer, VideoFormatContainer

from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class AbstractFFmpegBackend(AbstractBackend):
    """
    AbstractFFmpegBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    """

    ENCODING_SPEEDS = ["fast", "medium", "slow"]
    QUALITY_PRESETS = ["high", "medium", "low"]

    SUPPORTED_IN_AUDIO_FORMATS = {
        'aac': {},
        'ac3': {},
        'flac': {},
        'm4a': {},
        'mp3': {},
        'ogg': {},
        'opus': {},
        'wav': {},
        'wma': {},
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
        'wmv': {},
    }
    SUPPORTED_IN_FORMATS = SUPPORTED_IN_AUDIO_FORMATS | SUPPORTED_IN_VIDEO_FORMATS

    SUPPORTED_OUT_AUDIO_FORMATS = AudioFormatContainer.get_registered()
    SUPPORTED_OUT_VIDEO_FORMATS = VideoFormatContainer.get_registered()
    SUPPORTED_OUT_FORMATS = SUPPORTED_OUT_VIDEO_FORMATS | SUPPORTED_OUT_AUDIO_FORMATS

    @classmethod
    def __get_supported_codecs(cls, supported_format: dict[str, tuple[tuple, dict[str, Any]]], is_audio: bool, ext: str | None = None) -> Iterable[str]:
        res: set[str] = set()
        codecs_kwarg = "available_audio_codecs" if is_audio else "available_video_codecs"
        for cont_ext, data in supported_format.items():
            if not ext or (ext == cont_ext):
                _, kwargs = data
                res.update(kwargs[codecs_kwarg])
        return sorted(res)

    @classmethod
    def get_supported_audio_codecs(cls, ext: str | None = None) -> Iterable[str]:
        return cls.__get_supported_codecs(cls.SUPPORTED_OUT_FORMATS, is_audio=True, ext=ext)

    @classmethod
    def get_supported_video_codecs(cls, ext: str | None = None) -> Iterable[str]:
        return cls.__get_supported_codecs(cls.SUPPORTED_OUT_FORMATS, is_audio=False, ext=ext)

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
        self._install_deps = install_deps
        self._verbose = verbose

        # check ffmpeg
        self._ffmpeg_bin = self.find_in_path("ffmpeg")
        self._ffprobe_bin = self.find_in_path("ffprobe")


__all__ = [
    "AbstractFFmpegBackend",
]
