# src\file_conversor\backend\audio_video\format_container.py

from pathlib import Path
from typing import Iterable

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.audio_video.codec import _Codec, AudioCodec, VideoCodec

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FormatContainer:
    @staticmethod
    def _check_available_codec(codec: _Codec, available_codecs: Iterable[str]):
        if codec.name in available_codecs:
            return codec
        raise ValueError(f"Codec '{codec}' {_('not available. Available codecs are:')} {' '.join(available_codecs)}")

    def __init__(
        self,
        name: str,
        audio_codec: str = "null",
        video_codec: str = "null",
        available_audio_codecs: set[str] | None = None,
        available_video_codecs: set[str] | None = None,

    ) -> None:
        super().__init__()
        self._name = name
        self._available_audio_codecs = available_audio_codecs or set()
        self._available_video_codecs = available_video_codecs or set()

        self._available_audio_codecs.add("null")
        self._available_audio_codecs.add("copy")

        self._available_video_codecs.add("null")
        self._available_video_codecs.add("copy")

        self.audio_codec = AudioCodec.from_str(audio_codec)
        self.video_codec = VideoCodec.from_str(video_codec)

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
        if not isinstance(value, AudioCodec):
            raise ValueError(f"Cannot set '{type(value)}({value})' as audio codec.")
        self._check_available_codec(value, self._available_audio_codecs)
        self._audio_codec = value

    @property
    def video_codec(self):
        return self._video_codec

    @video_codec.setter
    def video_codec(self, value):
        if not isinstance(value, VideoCodec):
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
        res.extend(self.audio_codec.get_options())
        res.extend(self.video_codec.get_options())
        return res


AVAILABLE_AUDIO_CONTAINERS = {
    # AUDIO
    'mp3': FormatContainer(
        name="mp3",
        audio_codec="libmp3lame",
        available_audio_codecs={
            "libmp3lame"
        }
    ),
    'm4a': FormatContainer(
        name="ipod",
        audio_codec="aac",
        available_audio_codecs={
            "aac"
        }
    ),
    'ogg': FormatContainer(
        name="ogg",
        audio_codec="libvorbis",
        available_audio_codecs={
            "libvorbis"
        }
    ),
    'opus': FormatContainer(
        name="opus",
        audio_codec="libopus",
        available_audio_codecs={
            "libopus"
        }
    ),
    'flac': FormatContainer(
        name="flac",
        audio_codec="flac",
        available_audio_codecs={
            "flac"
        }
    ),
}

AVAILABLE_VIDEO_CONTAINERS = {
    # VIDEO
    'mp4': FormatContainer(
        name="mp4",
        audio_codec="aac",
        video_codec="libx264",
        available_audio_codecs={
            "aac",
            "ac3",
            "libmp3lame",
        },
        available_video_codecs={
            "libx264",
            "libx265",
            "h264_nvenc",
            "hevc_nvenc",
        },
    ),
    'avi': FormatContainer(
        name="avi",
        audio_codec="libmp3lame",
        video_codec="mpeg4",
        available_audio_codecs={
            "libmp3lame",
            "pcm_s16le",
        },
        available_video_codecs={
            "mpeg4",
        },
    ),
    'mkv': FormatContainer(
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
        },
        available_video_codecs={
            "libx264",
            "libx265",
            "h264_nvenc",
            "hevc_nvenc",
            "libvpx",
            "libvpx-vp9",
        },
    ),
    'webm': FormatContainer(
        name="webm",
        audio_codec="libvorbis",
        video_codec="libvpx",
        available_audio_codecs={
            "libvorbis",
            "libopus",
        },
        available_video_codecs={
            "libvpx",
            "libvpx-vp9",
        },
    ),
}
