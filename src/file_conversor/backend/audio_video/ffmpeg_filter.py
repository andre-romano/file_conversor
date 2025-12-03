# src\file_conversor\backend\audio_video\ffmpeg_filter.py

from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import parse_ffmpeg_filter
from file_conversor.utils.validators import check_valid_options

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegFilter:

    @classmethod
    def from_str(cls, filter: str):
        name, args, kwargs = parse_ffmpeg_filter(filter)
        return cls(name, *args, **kwargs)

    def __init__(self, name: str, *args: str, **options: str) -> None:
        super().__init__()
        self._name = name
        self._args = args
        self._options = options

    def __hash__(self) -> int:
        return hash(self._name) ^ hash(self._args) ^ hash(frozenset(self._options.items()))

    def __eq__(self, value: object) -> bool:
        if isinstance(value, FFmpegFilter):
            return (self._name == value._name) and (self._args == value._args) and (self._options == value._options)
        return False

    def __repr__(self) -> str:
        return self.get()

    def __str__(self) -> str:
        return f"{self._name}({", ".join(self._args)}{", ".join(f"{k}={v}" for k, v in self._options.items())})"

    def get(self) -> str:
        res = f"{self._name}" + ("=" if (self._args or self._options) else "")
        res += ":".join(self._args) + ("," if self._args and self._options else "")
        res += ":".join(f"{k}={v}" for k, v in self._options.items())
        return res


# BRIGHTNESS, CONTRAST, SATURATION, GAMMA
class FFmpegFilterEq(FFmpegFilter):
    def __init__(self, brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0, gamma: float = 1.0) -> None:
        super().__init__("eq", brightness=str(brightness - 1), contrast=str(contrast), saturation=str(saturation), gamma=str(gamma))


# RESIZE
class FFmpegFilterScale(FFmpegFilter):
    def __init__(self, width: int | str, height: int | str, force_original_aspect_ratio: str | None = None) -> None:
        options: dict[str, str] = {}
        if force_original_aspect_ratio:
            check_valid_options(force_original_aspect_ratio, {"increase", "decrease", "disable"})
            options["force_original_aspect_ratio"] = force_original_aspect_ratio
        super().__init__("scale", str(width), str(height), **options)


# ROTATE
class FFmpegFilterTranspose(FFmpegFilter):
    def __init__(self, direction: int) -> None:
        check_valid_options(direction, {0, 1, 2, 3})
        super().__init__("transpose", str(direction))


# MIRROR
class FFmpegFilterHflip(FFmpegFilter):
    def __init__(self) -> None:
        super().__init__("hflip")


class FFmpegFilterVflip(FFmpegFilter):
    def __init__(self) -> None:
        super().__init__("vflip")


# FPS
class FFmpegFilterMInterpolate(FFmpegFilter):
    def __init__(self, fps: int, mi_mode: str = "mci", mc_mode: str = "aobmc", me_mode: str = "bidir", vsbmc: int = 1) -> None:
        super().__init__("minterpolate", fps=str(fps), mi_mode=mi_mode, mc_mode=mc_mode, me_mode=me_mode, vsbmc=str(vsbmc))


# UNSHARP
class FFmpegFilterUnsharp(FFmpegFilter):
    def __init__(self, luma_msize_x: int = 5, luma_msize_y: int = 5, luma_amount: float = 1.0) -> None:
        super().__init__("unsharp", luma_msize_x=str(luma_msize_x), luma_msize_y=str(luma_msize_y), luma_amount=str(luma_amount))


# DESHAKE
class FFmpegFilterDeshake(FFmpegFilter):
    def __init__(self) -> None:
        super().__init__("deshake")


__all__ = [
    "FFmpegFilter",
    "FFmpegFilterEq",
    "FFmpegFilterScale",
    "FFmpegFilterTranspose",
    "FFmpegFilterHflip",
    "FFmpegFilterVflip",
    "FFmpegFilterMInterpolate",
    "FFmpegFilterUnsharp",
    "FFmpegFilterDeshake",
]
