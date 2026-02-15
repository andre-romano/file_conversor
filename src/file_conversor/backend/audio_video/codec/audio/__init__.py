# src\file_conversor\backend\audio_video\codec\audio\__init__.py

from enum import Enum

from file_conversor.backend.audio_video.codec.audio.ffmpeg_audio_codec import *


# register AUDIO codecs
class FFmpegAudioCodecs(Enum):
    NULL = "null"
    COPY = "copy"
    AAC_FDK = "libfdk_aac"
    AAC_LIB = "aac"
    AC3_LIB = "ac3"
    FLAC_LIB = "flac"
    MP3_LIB = "libmp3lame"
    OPUS_LIB = "libopus"
    VORBIS_LIB = "libvorbis"
    PCM_S16LE = "pcm_s16le"

    @property
    def codec(self) -> FFmpegAudioCodec:
        return FFmpegAudioCodec(self.value)


__all__ = [
    "FFmpegAudioCodec",
    "FFmpegAudioCodecs",
]
