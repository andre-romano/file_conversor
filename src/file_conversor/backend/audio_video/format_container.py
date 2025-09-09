# src\file_conversor\backend\audio_video\format_container.py

from pathlib import Path
from typing import Sequence

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.audio_video.codec import _Codec, AudioCodec, VideoCodec

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class _CodecProperty:
    def __init__(
        self,
        codec_type: type[VideoCodec | AudioCodec],
        codec: str | VideoCodec | AudioCodec = "null",
        available_codecs: Sequence[str | VideoCodec | AudioCodec] | None = None,
    ) -> None:
        super().__init__()
        self._codec_type = codec_type
        self._available_codecs = set([codec_type.from_str(c) if isinstance(c, str) else c for c in (available_codecs or [])])
        self._available_codecs.add(codec_type("null"))

        self.codec = codec

    @property
    def available_codecs(self) -> set[VideoCodec | AudioCodec]:
        return self._available_codecs

    @property
    def codec(self) -> _Codec:
        return self._codec

    @codec.setter
    def codec(self, value):
        if isinstance(value, self._codec_type):
            self._codec: _Codec = value
        elif isinstance(value, str):
            self._codec: _Codec = self._codec_type.from_str(value)
        else:
            raise TypeError(f"{_('Invalid codec type')} '{type(value)}: {value}'")
        if self._codec not in self._available_codecs:
            raise TypeError(f"{_('Unsupported codec')} '{value}' {_('for current container. Valid options are:')} {', '.join([str(c) for c in self._available_codecs])}")


class FormatContainer:

    def __init__(
        self,
        name: str,
        audio_codec: str | AudioCodec,
        available_audio_codecs: Sequence[str | AudioCodec],
        video_codec: str | VideoCodec = "null",
        available_video_codecs: Sequence[str | VideoCodec] | None = None,
    ) -> None:
        super().__init__()
        self._name = name
        self.audio = _CodecProperty(AudioCodec, audio_codec, available_audio_codecs)
        self.video = _CodecProperty(VideoCodec, video_codec, available_video_codecs)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, FormatContainer):
            return (self._name == value._name and
                    self.audio.codec == value.audio.codec and
                    self.video.codec == value.video.codec)
        return False

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"{self._name} (audio={self.audio.codec}, video={self.video.codec})"

    def __str__(self) -> str:
        return self._name

    def get_options(self) -> list[str]:
        res = ["-f", self._name]
        res.extend(self.audio.codec.get_options())
        res.extend(self.video.codec.get_options())
        return res


AVAILABLE_AUDIO_CONTAINERS = {
    # AUDIO
    'mp3': FormatContainer(
        name="mp3",
        audio_codec="libmp3lame",
        available_audio_codecs=[
            "libmp3lame"
        ]
    ),
    'm4a': FormatContainer(
        name="ipod",
        audio_codec="aac",
        available_audio_codecs=[
            "aac"
        ]
    ),
    'ogg': FormatContainer(
        name="ogg",
        audio_codec="libvorbis",
        available_audio_codecs=[
            "libvorbis"
        ]
    ),
    'opus': FormatContainer(
        name="opus",
        audio_codec="libopus",
        available_audio_codecs=[
            "libopus"
        ]
    ),
    'flac': FormatContainer(
        name="flac",
        audio_codec="flac",
        available_audio_codecs=[
            "flac"
        ]
    ),
}

AVAILABLE_VIDEO_CONTAINERS = {
    # VIDEO
    'mp4': FormatContainer(
        name="mp4",
        audio_codec="aac",
        video_codec="libx264",
        available_audio_codecs=[
            "aac",
            "ac3",
            "libmp3lame",
        ],
        available_video_codecs=[
            "libx264",
            "libx265",
            "h264_nvenc",
            "hevc_nvenc",
        ],
    ),
    'avi': FormatContainer(
        name="avi",
        audio_codec="libmp3lame",
        video_codec="mpeg4",
        available_audio_codecs=[
            "libmp3lame",
            "pcm_s16le",
        ],
        available_video_codecs=[
            "mpeg4",
        ],
    ),
    'mkv': FormatContainer(
        name="matroska",
        audio_codec="aac",
        video_codec="libx264",
        available_audio_codecs=[
            "aac",
            "ac3",
            "libmp3lame",
            "libopus",
            "libvorbis",
            "flac",
        ],
        available_video_codecs=[
            "libx264",
            "libx265",
            "h264_nvenc",
            "hevc_nvenc",
            "libvpx",
            "libvpx-vp9",
        ],
    ),
    'webm': FormatContainer(
        name="webm",
        audio_codec="libvorbis",
        video_codec="libvpx",
        available_audio_codecs=[
            "libvorbis",
            "libopus",
        ],
        available_video_codecs=[
            "libvpx",
            "libvpx-vp9",
        ],
    ),
}
