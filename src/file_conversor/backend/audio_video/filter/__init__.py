# src\file_conversor\backend\audio_video\filter\__init__.py


# user-provided imports
from file_conversor.backend.audio_video.filter.ffmpeg_filter import *
from file_conversor.utils.validators import check_valid_options


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
