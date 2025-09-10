# src\file_conversor\backend\audio_video\ffmpeg_filter.py

from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_valid_options

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class FFmpegFilter:
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

    def get(self) -> str:
        res = f"{self._name}" + ("=" if (self._args or self._options) else "")
        if self._args:
            res += ":".join(self._args)
        if self._options:
            if self._args:
                res += ","
            res += ":".join(f"{k}={v}" for k, v in self._options.items())
        return res


# BRIGHTNESS, CONTRAST, SATURATION, GAMMA
def FFmpegFilterEq(brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0, gamma: float = 1.0) -> FFmpegFilter:
    return FFmpegFilter("eq", brightness=str(brightness - 1), contrast=str(contrast), saturation=str(saturation), gamma=str(gamma),)


# RESIZE
def FFmpegFilterScale(width: int | str, height: int | str, force_original_aspect_ratio: str | None = None) -> FFmpegFilter:
    options: dict[str, str] = {}
    if force_original_aspect_ratio:
        check_valid_options(force_original_aspect_ratio, {"increase", "decrease", "disable"})
        options["force_original_aspect_ratio"] = force_original_aspect_ratio
    return FFmpegFilter("scale", str(width), str(height), **options)


# ROTATE
def FFmpegFilterTranspose(direction: int) -> FFmpegFilter:
    check_valid_options(direction, {0, 1, 2, 3})
    return FFmpegFilter("transpose", str(direction))


# MIRROR
def FFmpegFilterHflip() -> FFmpegFilter:
    return FFmpegFilter("hflip")


def FFmpegFilterVflip() -> FFmpegFilter:
    return FFmpegFilter("vflip")


# FPS
def FFmpegFilterMInterpolate(fps: int, mi_mode: str = "mci", mc_mode: str = "aobmc", me_mode: str = "bidir", vsbmc: int = 1) -> FFmpegFilter:
    return FFmpegFilter("minterpolate", fps=str(fps), mi_mode=mi_mode, mc_mode=mc_mode, me_mode=me_mode, vsbmc=str(vsbmc))


# UNSHARP
def FFmpegFilterUnsharp(luma_msize_x: int = 5, luma_msize_y: int = 5, luma_amount: float = 1.0) -> FFmpegFilter:
    return FFmpegFilter("unsharp", luma_msize_x=str(luma_msize_x), luma_msize_y=str(luma_msize_y), luma_amount=str(luma_amount))


# DESHAKE
def FFmpegFilterDeshake() -> FFmpegFilter:
    return FFmpegFilter("deshake")
