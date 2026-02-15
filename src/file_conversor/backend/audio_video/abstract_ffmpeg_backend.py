# src\file_conversor\backend\audio_video\abstract_ffmpeg_backend.py

from enum import Enum
from typing import cast

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.audio_video.container import (
    AudioFormatContainers,
    VideoFormatContainers,
)
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class AbstractFFmpegBackend(AbstractBackend):
    """
    AbstractFFmpegBackend is a class that provides an interface for handling audio and video files using FFmpeg.
    """

    class SupportedInAudioFormats(Enum):
        AAC = "aac"
        AC3 = "ac3"
        FLAC = "flac"
        M4A = "m4a"
        MP3 = "mp3"
        OGG = "ogg"
        OPUS = "opus"
        WAV = "wav"
        WMA = "wma"

    class SupportedInVideoFormats(Enum):
        _3GP = "3gp"
        ASF = "asf"
        AVI = "avi"
        FLV = "flv"
        H264 = "h264"
        HEVC = "hevc"
        M4V = "m4v"
        MKV = "mkv"
        MOV = "mov"
        MP4 = "mp4"
        MPEG = "mpeg"
        MPG = "mpg"
        WEBM = "webm"
        WMV = "wmv"

    SupportedInFormats = cast(type[Enum], Enum("SupportedInFormats", {
        **{fmt.name: fmt.value for fmt in SupportedInAudioFormats},
        **{fmt.name: fmt.value for fmt in SupportedInVideoFormats},
    }))

    SupportedOutAudioFormats = AudioFormatContainers
    SupportedOutVideoFormats = VideoFormatContainers
    SupportedOutFormats = cast(type[Enum], Enum("SupportedOutFormats", {
        **{fmt.name: fmt.value for fmt in SupportedOutAudioFormats},
        **{fmt.name: fmt.value for fmt in SupportedOutVideoFormats},
    }))

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
