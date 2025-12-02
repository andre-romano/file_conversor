# src\file_conversor\backend\audio_video\format_container.py

from pathlib import Path
from typing import Any, Iterable, Self

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.audio_video.ffmpeg_codec import _FFmpegCodec, FFmpegAudioCodec, FFmpegVideoCodec

from file_conversor.utils import AbstractRegisterManager

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FormatContainer(AbstractRegisterManager):
    @staticmethod
    def _check_available_codec(codec: _FFmpegCodec, available_codecs: Iterable[str]):
        if codec.name in available_codecs:
            return codec
        raise ValueError(f"Codec '{codec}' {_('not available. Available codecs are:')} {', '.join(available_codecs)}")

    def __init__(
        self,
        name: str,
        audio_codec: str,
        video_codec: str,
        available_audio_codecs: set[str],
        available_video_codecs: set[str],

    ) -> None:
        super().__init__()
        self._name = name
        self._available_audio_codecs = available_audio_codecs
        self._available_video_codecs = available_video_codecs

        self.audio_codec = FFmpegAudioCodec.from_str(audio_codec)
        self.video_codec = FFmpegVideoCodec.from_str(video_codec)

    # PROPERTIES
    @property
    def available_audio_codecs(self):
        return self._available_audio_codecs.copy()

    @property
    def available_video_codecs(self):
        return self._available_video_codecs.copy()

    @property
    def audio_codec(self):
        return self._audio_codec

    @audio_codec.setter
    def audio_codec(self, value):
        if not isinstance(value, FFmpegAudioCodec):
            raise ValueError(f"Cannot set '{type(value)}({value})' as audio codec.")
        self._check_available_codec(value, self._available_audio_codecs)
        self._audio_codec = value

    @property
    def video_codec(self):
        return self._video_codec

    @video_codec.setter
    def video_codec(self, value):
        if not isinstance(value, FFmpegVideoCodec):
            raise ValueError(f"Cannot set '{type(value)}({value})' as video codec.")
        self._check_available_codec(value, self._available_video_codecs)
        self._video_codec = value

    # METHODS
    def __eq__(self, value: object) -> bool:
        if isinstance(value, FormatContainer):
            return (self._name == value._name and
                    self.audio_codec == value.audio_codec and
                    self.video_codec == value.video_codec)
        return False

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"{self._name} (audio={self.audio_codec}, video={self.video_codec})"

    def __str__(self) -> str:
        return self._name

    def get_options(self) -> list[str]:
        res = ["-f", self._name]
        if self._name.lower() != "null":
            res.extend(self.audio_codec.get_options())
            res.extend(self.video_codec.get_options())
        return res


class VideoFormatContainer(FormatContainer):
    _REGISTERED: dict[str, tuple[tuple, dict[str, Any]]] = {}


class AudioFormatContainer(FormatContainer):
    _REGISTERED: dict[str, tuple[tuple, dict[str, Any]]] = {}


# AUDIO CONTAINERS
AudioFormatContainer.register(
    "null",
    name="null",
    audio_codec="null",
    video_codec="null",
    available_audio_codecs={
        "null", "copy",
    },
    available_video_codecs={
        "null", "copy",
    },
)
AudioFormatContainer.register(
    'mp3',
    name="mp3",
    audio_codec="libmp3lame",
    video_codec="null",
    available_audio_codecs={
        "libmp3lame",
        "copy",
    },
    available_video_codecs={
        "null",
    },
)
AudioFormatContainer.register(
    'm4a',
    name="ipod",
    audio_codec="aac",
    video_codec="null",
    available_audio_codecs={
        "aac",
        "copy",
    },
    available_video_codecs={
        "null",
    },
)
AudioFormatContainer.register(
    'ogg',
    name="ogg",
    audio_codec="libvorbis",
    video_codec="null",
    available_audio_codecs={
        "libvorbis",
        "copy",
    },
    available_video_codecs={
        "null",
    },
)
AudioFormatContainer.register(
    'opus',
    name="opus",
    audio_codec="libopus",
    video_codec="null",
    available_audio_codecs={
        "libopus",
        "copy",
    },
    available_video_codecs={
        "null",
    },
)
AudioFormatContainer.register(
    'flac',
    name="flac",
    audio_codec="flac",
    video_codec="null",
    available_audio_codecs={
        "flac",
        "copy",
    },
    available_video_codecs={
        "null",
    },
)

# VIDEO CONTAINERS
VideoFormatContainer.register(
    "null",
    name="null",
    audio_codec="null",
    video_codec="null",
    available_audio_codecs={
        "null", "copy",
    },
    available_video_codecs={
        "null", "copy",
    },
)
VideoFormatContainer.register(
    'mp4',
    name="mp4",
    audio_codec="aac",
    video_codec="libx264",
    available_audio_codecs={
        "aac",
        "ac3",
        "libmp3lame",
        "null", "copy",
    },
    available_video_codecs={
        "libx264",
        "libx265",

        "h264_nvenc",
        "hevc_nvenc",

        "h264_vaapi",
        "hevc_vaapi",

        "h264_qsv",
        "hevc_qsv",

        "copy",
    },
)
VideoFormatContainer.register(
    'avi',
    name="avi",
    audio_codec="libmp3lame",
    video_codec="mpeg4",
    available_audio_codecs={
        "libmp3lame",
        "pcm_s16le",
        "null", "copy",
    },
    available_video_codecs={
        "mpeg4",
        "copy",
    },
)
VideoFormatContainer.register(
    'mkv',
    name="matroska",
    audio_codec="aac",
    video_codec="libx264",
    available_audio_codecs={
        "aac",
        "ac3",
        "libmp3lame",
        "libopus",
        "libvorbis",
        "flac",
        "null", "copy",
    },
    available_video_codecs={
        "libx264",
        "libx265",

        "h264_nvenc",
        "hevc_nvenc",

        "h264_vaapi",
        "hevc_vaapi",

        "h264_qsv",
        "hevc_qsv",

        "libvpx",
        "libvpx-vp9",
        "libaom-av1",

        "vp8_vaapi",
        "vp9_vaapi",

        "vp8_qsv",
        "vp9_qsv",

        "av1_nvenc",
        "av1_vaapi",
        "av1_qsv",

        "copy",
    },
)
VideoFormatContainer.register(
    'webm',
    name="webm",
    audio_codec="libvorbis",
    video_codec="libvpx",
    available_audio_codecs={
        "libvorbis",
        "libopus",
        "null", "copy",
    },
    available_video_codecs={
        "libvpx",
        "libvpx-vp9",
        "libaom-av1",

        "vp8_vaapi",
        "vp9_vaapi",

        "vp8_qsv",
        "vp9_qsv",

        "av1_nvenc",
        "av1_vaapi",
        "av1_qsv",

        "copy",
    },
)

__all__ = [
    "FormatContainer",
    "VideoFormatContainer",
    "AudioFormatContainer",
]
