# src\file_conversor\backend\audio_video\container\audio_format_container.py

from enum import StrEnum
from typing import Any, Self, override

from file_conversor.backend.audio_video.codec import FFmpegAudioCodecs
from file_conversor.backend.audio_video.container.format_container import (
    FormatContainer,
)

# user-provided imports
from file_conversor.config import LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioFormatContainers(StrEnum):
    NULL = "null"
    MP3 = "mp3"
    M4A = "m4a"
    OGG = "ogg"
    OPUS = "opus"
    FLAC = "flac"

    @property
    def container(self) -> FormatContainer:
        match self:
            case self.NULL:
                return FormatContainer("null")
            case self.MP3:
                return FormatContainer("mp3", audio_codec=FFmpegAudioCodecs.MP3_LIB)
            case self.M4A:
                return FormatContainer("ipod", audio_codec=FFmpegAudioCodecs.AAC_LIB)
            case self.OGG:
                return FormatContainer("ogg", audio_codec=FFmpegAudioCodecs.VORBIS_LIB)
            case self.OPUS:
                return FormatContainer("opus", audio_codec=FFmpegAudioCodecs.OPUS_LIB)
            case self.FLAC:
                return FormatContainer("flac", audio_codec=FFmpegAudioCodecs.FLAC_LIB)

    @override
    def __contains__(self, value: str | Self | Any) -> bool:
        if isinstance(value, str):
            return value.lower() == self.value
        if isinstance(value, AudioFormatContainers):
            return value == self
        raise ValueError(_("Value must be a string or an instance of AudioFormatContainers"))


__all__ = [
    "AudioFormatContainers",
]
