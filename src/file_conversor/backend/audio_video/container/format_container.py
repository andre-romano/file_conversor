# src\file_conversor\backend\audio_video\format_container.py

from typing import override

from file_conversor.backend.audio_video.codec import (
    FFmpegAudioCodec,
    FFmpegAudioCodecs,
    FFmpegVideoCodec,
    FFmpegVideoCodecs,
)
from file_conversor.config import Log, get_translation


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FormatContainer:
    def __init__(
        self,
        name: str,
        audio_codec: FFmpegAudioCodecs = FFmpegAudioCodecs.NULL,
        video_codec: FFmpegVideoCodecs = FFmpegVideoCodecs.NULL,
        available_audio_codecs: set[FFmpegAudioCodecs] | None = None,
        available_video_codecs: set[FFmpegVideoCodecs] | None = None,
    ) -> None:
        super().__init__()
        self._name = name

        self._available_audio_codecs: set[FFmpegAudioCodecs] = {
            audio_codec, FFmpegAudioCodecs.NULL, FFmpegAudioCodecs.COPY,
        }.union(available_audio_codecs or set())

        self._available_video_codecs: set[FFmpegVideoCodecs] = {
            video_codec, FFmpegVideoCodecs.NULL, FFmpegVideoCodecs.COPY
        }.union(available_video_codecs or set())

        self._audio_codec = FFmpegAudioCodecs.NULL.codec
        self._video_codec = FFmpegVideoCodecs.NULL.codec

        self.audio_codec = audio_codec.codec
        self.video_codec = video_codec.codec

    # PROPERTIES
    @property
    def available_audio_codecs(self):
        return self._available_audio_codecs.copy()

    @property
    def available_video_codecs(self):
        return self._available_video_codecs.copy()

    @property
    def audio_codec(self) -> FFmpegAudioCodec:
        return self._audio_codec

    @audio_codec.setter
    def audio_codec(self, value: FFmpegAudioCodec):
        codec_enum = FFmpegAudioCodecs(value.name)
        if codec_enum not in self._available_audio_codecs:
            raise ValueError(f"Codec '{value.name}' {_('not available. Available codecs are:')} {', '.join(c.name for c in self._available_audio_codecs)}")
        self._audio_codec = value

    @property
    def video_codec(self) -> FFmpegVideoCodec:
        return self._video_codec

    @video_codec.setter
    def video_codec(self, value: FFmpegVideoCodec):
        codec_enum = FFmpegVideoCodecs(value.name)
        if codec_enum not in self._available_video_codecs:
            raise ValueError(f"Codec '{value.name}' {_('not available. Available codecs are:')} {', '.join(c.name for c in self._available_video_codecs)}")
        self._video_codec = value

    # METHODS
    @override
    def __eq__(self, value: object) -> bool:
        if isinstance(value, FormatContainer):
            return (self._name == value._name and
                    self.audio_codec == value.audio_codec and
                    self.video_codec == value.video_codec)
        return False

    @override
    def __hash__(self) -> int:
        return hash(self._name)

    @override
    def __repr__(self) -> str:
        return f"{self._name} (audio={self.audio_codec}, video={self.video_codec})"

    @override
    def __str__(self) -> str:
        return self._name

    def get_options(self) -> list[str]:
        res = ["-f", self._name]
        if self._name.lower() != "null":
            res.extend(self.audio_codec.get_options())
            res.extend(self.video_codec.get_options())
        return res

    def copy(self) -> "FormatContainer":
        return FormatContainer(
            name=self._name,
            audio_codec=FFmpegAudioCodecs(self.audio_codec.name),
            video_codec=FFmpegVideoCodecs(self.video_codec.name),
            available_audio_codecs=self._available_audio_codecs,
            available_video_codecs=self._available_video_codecs,
        )


__all__ = [
    "FormatContainer",
]
