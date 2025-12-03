# src\file_conversor\backend\audio_video\codec.py

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Self

# user-provided imports
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter

from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import AbstractRegisterManager

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class _FFmpegCodec(AbstractRegisterManager):
    @classmethod
    def get_available_codecs(cls) -> dict[str, Any]:
        return cls.get_registered()

    def __init__(
        self,
        invalid_prefix: str,
        prefix: str,
        name: str,
        options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._invalid_prefix = invalid_prefix
        self._prefix = prefix
        self._name = name
        self._options: dict[str, str | int | None] = {}
        self.update(options or {})

    # PROPERTIES
    @property
    def name(self):
        return self._name

    # DUNDER METHODS
    def __eq__(self, value: object) -> bool:
        if isinstance(value, _FFmpegCodec):
            return (self._name == value._name)
        return False

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"{self._name} ({' '.join(self.get_options())})"

    def __str__(self) -> str:
        return self._name

    # METHODS
    def update(self, options: dict[str, Any]):
        for opt, val in options.items():
            self.set(opt, val)

    def add(self, option: str, value: Any = None):
        if option in self._options:
            if value:
                self._options[option] = f"{self._options[option]},{value}"
        else:
            self.set(option, value)

    def set(self, option: str, value: Any = None):
        self._options[option] = value

    def unset(self, option: str):
        if option in self._options:
            del self._options[option]

    def set_bitrate(self, bitrate: int):
        raise NotImplementedError("not implemented")

    def set_filters(self, *filters: FFmpegFilter):
        raise NotImplementedError("not implemented")

    def get_options(self) -> list[str]:
        res = [self._prefix, self._name]
        if not self._name or self._name.lower() == "null":
            return [self._invalid_prefix]
        if self._name.lower() == "copy":
            return res
        for key, value in self._options.items():
            if value:
                res.extend([str(key), str(value)])
                continue
            res.extend([str(key)])
        return res


class FFmpegAudioCodec(_FFmpegCodec):
    _REGISTERED: dict[str, tuple[tuple, dict[str, Any]]] = {}

    def __init__(
        self,
        name: str,
        options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(invalid_prefix="-an", prefix="-c:a",
                         name=name,
                         options=options,
                         )

    def set_bitrate(self, bitrate: int):
        self.set("-b:a", f"{bitrate}k")

    def set_filters(self, *filters: FFmpegFilter):
        for filter in filters:
            self.add("-af", filter.get())


class FFmpegVideoCodec(_FFmpegCodec):
    _REGISTERED: dict[str, tuple[tuple, dict[str, Any]]] = {}

    def __init__(
        self,
        name: str,
        options: dict[str, Any] | None = None,
        encoding_speed_opts: dict[str, dict[str, Any]] | None = None,
        quality_setting_opts: dict[str, dict[str, Any]] | None = None,
        profile_opts: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(invalid_prefix="-vn", prefix="-c:v",
                         name=name,
                         options=options,
                         )
        self._encoding_speed_opts = encoding_speed_opts or {}
        self._quality_setting_opts = quality_setting_opts or {}
        self._profile_opts = profile_opts or {}

    def set_profile(self, profile: str):
        if profile not in self._profile_opts:
            logger.warning(f"'{profile}' {_("profile not available for codec")} '{self._name}'")
            return
        self.update(self._profile_opts[profile])

    def set_encoding_speed(self, speed: str):
        if speed not in self._encoding_speed_opts:
            logger.warning(f"'{speed}' {_("speed not available for codec")} '{self._name}'")
            return
        self.update(self._encoding_speed_opts[speed])

    def set_quality_setting(self, quality: str):
        if quality not in self._quality_setting_opts:
            logger.warning(f"'{quality}' {_("quality not available for codec")} '{self._name}'")
            return
        self.update(self._quality_setting_opts[quality])
        self.unset("-b:v")  # remove bitrate if set

    def set_bitrate(self, bitrate: int):
        self.set("-b:v", f"{bitrate}k")

    def set_filters(self, *filters: FFmpegFilter):
        for filter in filters:
            self.add("-vf", filter.get())


# register AUDIO codecs
FFmpegAudioCodec.register("null", name="null")
FFmpegAudioCodec.register("copy", name="copy")
FFmpegAudioCodec.register("aac", name="aac")
FFmpegAudioCodec.register("ac3", name="ac3")
FFmpegAudioCodec.register("flac", name="flac")
FFmpegAudioCodec.register("libfdk_aac", name="libfdk_aac")
FFmpegAudioCodec.register("libmp3lame", name="libmp3lame")
FFmpegAudioCodec.register("libopus", name="libopus")
FFmpegAudioCodec.register("libvorbis", name="libvorbis")
FFmpegAudioCodec.register("pcm_s16le", name="pcm_s16le")


# register VIDEO codec quality options
class QualityOptions:
    def __init__(
        self,
        high: str,
        medium: str,
        low: str,
    ):
        super().__init__()
        self.high = high
        self.medium = medium
        self.low = low

    def _get_quality_lib(self) -> dict[str, dict[str, str]]:
        return {
            "high": {"-crf": self.high},
            "medium": {"-crf": self.medium},
            "low": {"-crf": self.low},
        }

    def _get_quality_nvenc(self) -> dict[str, dict[str, str]]:
        return {
            "high": {"-cq": self.high},
            "medium": {"-cq": self.medium},
            "low": {"-cq": self.low},
        }

    def _get_quality_vaapi(self) -> dict[str, dict[str, str]]:
        return {
            "high": {"-qp": self.high},
            "medium": {"-qp": self.medium},
            "low": {"-qp": self.low},
        }

    def _get_quality_qsv(self) -> dict[str, dict[str, str]]:
        return {
            "high": {"-global_quality": self.high},
            "medium": {"-global_quality": self.medium},
            "low": {"-global_quality": self.low},
        }

    def get_quality(self, impl: str) -> dict[str, dict[str, str]]:
        if impl == "lib":
            return self._get_quality_lib()
        elif impl == "nvenc":
            return self._get_quality_nvenc()
        elif impl == "vaapi":
            return self._get_quality_vaapi()
        elif impl == "qsv":
            return self._get_quality_qsv()
        raise ValueError(f"Unknown implementation: {impl}")


# register VIDEO codecs
FFmpegVideoCodec.register("null", name="null")
FFmpegVideoCodec.register("copy", name="copy")

for codec_name, impl in [("h264_nvenc", "nvenc"), ("hevc_nvenc", "nvenc"),
                         ("h264_vaapi", "vaapi"), ("hevc_vaapi", "vaapi"),
                         ("h264_qsv", "qsv"), ("hevc_qsv", "qsv"),
                         ("libx264", "lib"), ("libx265", "lib"),
                         ]:
    preset = "-preset"
    profile_v = "-profile:v"
    FFmpegVideoCodec.register(codec_name, name=codec_name,
                              quality_setting_opts=QualityOptions(**{
                                  "high": "18",
                                  "medium": "23",
                                  "low": "28",
                              }).get_quality(impl),
                              encoding_speed_opts={
                                  "fast": {preset: "fast"},
                                  "medium": {preset: "medium"},
                                  "slow": {preset: "slow"},
                              },
                              profile_opts={
                                  "high": {profile_v: "high"},
                                  "medium": {profile_v: "main"},
                                  "low": {profile_v: "baseline"},
                              },
                              )


for codec_name, impl in [("vp8_vaapi", "vaapi"), ("vp9_vaapi", "vaapi"),
                         ("vp8_qsv", "qsv"), ("vp9_qsv", "qsv"),
                         ("libvpx", "lib"), ("libvpx-vp9", "lib"),
                         ]:
    FFmpegVideoCodec.register(codec_name, name=codec_name,
                              quality_setting_opts=QualityOptions(**{
                                  "high": "13",
                                  "medium": "35",
                                  "low": "55",
                              }).get_quality(impl),
                              )

for codec_name, impl in [("av1_nvenc", "nvenc"),
                         ("av1_vaapi", "vaapi"),
                         ("av1_qsv", "qsv"),
                         ("libaom-av1", "lib"),
                         ]:
    FFmpegVideoCodec.register(codec_name, name=codec_name,
                              quality_setting_opts=QualityOptions(**{
                                  "high": "19",
                                  "medium": "29",
                                  "low": "42",
                              }).get_quality(impl),
                              )

FFmpegVideoCodec.register("mpeg4", name="mpeg4")

__all__ = [
    "FFmpegAudioCodec",
    "FFmpegVideoCodec",
]
