# src\file_conversor\backend\audio_video\codec.py

import copy

from pathlib import Path
from typing import Any, Callable, Iterable, Self

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class _Codec:
    AVAILABLE_CODECS: dict[str, Self] = {}

    @classmethod
    def register(cls, name: str, *args, **kwargs):
        codec = cls(name=name, *args, **kwargs)
        cls.AVAILABLE_CODECS[name] = codec

    @classmethod
    def from_str(cls, name: str) -> Self:
        if name not in cls.AVAILABLE_CODECS:
            raise ValueError(f"Invalid codec '{name}'. Available codecs: {', '.join(cls.AVAILABLE_CODECS)}")
        return copy.deepcopy(cls.AVAILABLE_CODECS[name])

    def __init__(
        self,
        invalid_prefix: str,
        prefix: str,
        name: str,
        valid_options: Iterable[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self._invalid_prefix = invalid_prefix
        self._prefix = prefix
        self._name = name
        self._options: dict[str, str | int | None] = {}
        self._valid_options = set(valid_options or [])
        self._update(kwargs)

    # PROPERTIES
    @property
    def name(self):
        return self._name

    # DUNDER METHODS
    def __eq__(self, value: object) -> bool:
        if isinstance(value, _Codec):
            return (self._name == value._name)
        return False

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"{self._name} ({' '.join(self.get_options())})"

    def __str__(self) -> str:
        return self._name

    # METHODS
    def _update(self, options: dict[str, Any]):
        for opt, val in options.items():
            self._set(opt, val)

    def _set(self, option: str, value: Any = None):
        if option not in self._valid_options:
            raise KeyError(f"{_('Invalid option')} '{option}' {_('for codec')} '{self._name}'. {_('Valid options are:')} {', '.join(self._valid_options)}")
        if option in self._options and value:
            self._options[option] = f"{self._options[option]},{value}"
        else:
            self._options[option] = value

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


class AudioCodec(_Codec):
    AVAILABLE_CODECS: dict[str, Self] = {}

    def __init__(self, name: str, valid_options: Iterable[str] | None = None, **kwargs) -> None:
        super().__init__(invalid_prefix="-an", prefix="-c:a", name=name, valid_options=valid_options, **kwargs)
        self._valid_options.add("-b:a")

    def set_bitrate(self, bitrate: int):
        self._set("-b:a", f"{bitrate}k")


class VideoCodec(_Codec):
    AVAILABLE_CODECS: dict[str, Self] = {}

    def __init__(self, name: str, valid_options: Iterable[str] | None = None, **kwargs) -> None:
        super().__init__(invalid_prefix="-vn", prefix="-c:v", name=name, valid_options=valid_options, **kwargs)
        self._valid_options.add("-b:v")
        self._valid_options.add("-r")
        self._valid_options.add("-vf")

    def set_bitrate(self, bitrate: int):
        self._set("-b:v", f"{bitrate}k")

    def set_fps(self, fps: int):
        self._set("-r", f"{fps}")

    def set_resolution(self, width: int, height: int):
        self._set("-vf", rf"scale={width}:{height}")

    def set_rotation(self, rotation: int):
        video_filter = ""
        if rotation in (90, -270):
            video_filter = "transpose=1"  # 90deg rot clockwise
        elif rotation in (180, -180):
            video_filter = "transpose=1,transpose=1"  # 180deg rot clockwise
        elif rotation in (270, -90):
            video_filter = "transpose=2"  # -90deg rot clockwise
        else:
            raise ValueError(f"{_('Invalid rotation')} '{rotation}'. {_('Valid options are:')} -270, -180, -90, 90, 180, 270.")
        self._set("-vf", video_filter)

    def set_mirror(self, mirror_axis: str):
        self._set("-vf", "hflip" if mirror_axis.lower() == "x" else "vflip")


# register AUDIO codecs
AudioCodec.register("null")
AudioCodec.register("copy")
AudioCodec.register("aac")
AudioCodec.register("ac3")
AudioCodec.register("flac")
AudioCodec.register("libfdk_aac")
AudioCodec.register("libmp3lame")
AudioCodec.register("libopus")
AudioCodec.register("libvorbis")
AudioCodec.register("pcm_s16le")

# register AUDIO codecs
VideoCodec.register("null")
VideoCodec.register("copy")
VideoCodec.register("h264_nvenc", valid_options={
    "-preset": [
        "medium"
    ]
})
VideoCodec.register("hevc_nvenc", valid_options={
    "-preset": [
        "medium"
    ]
})
VideoCodec.register("libx264", valid_options={
    "-preset": [
        "medium"
    ]
})
VideoCodec.register("libx265", valid_options={
    "-preset": [
        "medium"
    ]
})
VideoCodec.register("libvpx")
VideoCodec.register("libvpx-vp9")
VideoCodec.register("mpeg4")
