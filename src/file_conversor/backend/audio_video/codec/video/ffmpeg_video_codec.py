# src\file_conversor\backend\audio_video\codec.py

from enum import Enum
from typing import Any, override

from file_conversor.backend.audio_video.codec.abstract_ffmpeg_codec import (
    AbstractFFmpegCodec,
)
from file_conversor.backend.audio_video.filter.ffmpeg_filter import FFmpegFilter
from file_conversor.config import Environment, Log, get_translation


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegVideoCodec(AbstractFFmpegCodec):
    class ProfileSetting(Enum):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    class QualitySetting(Enum):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    class EncodingSetting(Enum):
        FAST = "fast"
        MEDIUM = "medium"
        SLOW = "slow"

    @classmethod
    def get_cpu_count(cls) -> int:
        return Environment.get_cpu_count()

    def __init__(
        self,
        name: str,
        options: dict[str, Any] | None = None,
        encoding_speed_opts: dict[EncodingSetting, dict[str, Any]] | None = None,
        quality_setting_opts: dict[QualitySetting, dict[str, Any]] | None = None,
        profile_opts: dict[ProfileSetting, dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(invalid_prefix="-vn", prefix="-c:v",
                         name=name,
                         options=options,
                         )
        self._encoding_speed_opts = encoding_speed_opts or {}
        self._quality_setting_opts = quality_setting_opts or {}
        self._profile_opts = profile_opts or {}

    def set_profile(self, profile: ProfileSetting):
        if profile not in self._profile_opts:
            logger.warning(f"'{profile}' {_("profile not available for codec")} '{self._name}'")
            return
        self.update(self._profile_opts[profile])

    def set_encoding_speed(self, speed: EncodingSetting):
        if speed not in self._encoding_speed_opts:
            logger.warning(f"'{speed}' {_("speed not available for codec")} '{self._name}'")
            return
        self.update(self._encoding_speed_opts[speed])

    def set_quality_setting(self, quality: QualitySetting):
        if quality not in self._quality_setting_opts:
            logger.warning(f"'{quality}' {_("quality not available for codec")} '{self._name}'")
            return
        self.update(self._quality_setting_opts[quality])

    @override
    def set_bitrate(self, bitrate: int):
        self._set_bitrate("-b:v", bitrate)

    @override
    def set_filters(self, *filters: FFmpegFilter):
        self._set_filters("-vf", *filters)


__all__ = [
    "FFmpegVideoCodec",
]
