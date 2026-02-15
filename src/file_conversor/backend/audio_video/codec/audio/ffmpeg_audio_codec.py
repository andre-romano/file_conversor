# src\file_conversor\backend\audio_video\codec.py

from typing import Any, override

# user-provided imports
from file_conversor.backend.audio_video.codec.abstract_ffmpeg_codec import (
    AbstractFFmpegCodec,
)
from file_conversor.backend.audio_video.filter.ffmpeg_filter import FFmpegFilter
from file_conversor.config import Log, get_translation

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegAudioCodec(AbstractFFmpegCodec):

    def __init__(
        self,
        name: str,
        options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(invalid_prefix="-an", prefix="-c:a",
                         name=name,
                         options=options,
                         )

    @override
    def set_bitrate(self, bitrate: int):
        self._set_bitrate("-b:a", bitrate)

    @override
    def set_filters(self, *filters: FFmpegFilter):
        self._set_filters("-af", *filters)


__all__ = [
    "FFmpegAudioCodec",
]
