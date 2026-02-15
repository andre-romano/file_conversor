# src\file_conversor\backend\audio_video\codec\_mpeg.py

from enum import Enum

# user-provided imports
from file_conversor.backend.audio_video.codec.video.ffmpeg_video_codec import FFmpegVideoCodec


class MpegCodecs(Enum):
    MPEG4 = "mpeg4"

    @property
    def codec(self) -> FFmpegVideoCodec:
        return FFmpegVideoCodec(self.value)


__all__ = [
    "MpegCodecs",
]
