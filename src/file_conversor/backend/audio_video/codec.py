# src\file_conversor\backend\audio_video\codec.py

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
    def register(cls, name, *args, **kwargs):
        codec = cls(name=name, *args, **kwargs)
        cls.AVAILABLE_CODECS[name] = codec

    @classmethod
    def from_str(cls, codec: str) -> Self:
        return cls.AVAILABLE_CODECS[codec]

    def __init__(self, invalid_prefix: str, prefix: str, name: str, valid_options: Iterable[str] | None = None, **kwargs) -> None:
        super().__init__()
        self._invalid_prefix = invalid_prefix
        self._prefix = prefix
        self._name = name
        self._options = {}
        self._valid_options = set(valid_options or [])
        self.update(kwargs)

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

    @property
    def name(self):
        return self._name

    def set(self, option: str, value: Any = None):
        if option not in self._valid_options:
            raise KeyError(f"{_('Invalid option')} '{option}' {_('for codec')} '{self._name}'. {_('Valid options are:')} {', '.join(self._valid_options)}")
        self._options[option] = value

    def set_bitrate(self, bitrate: int):
        raise NotImplementedError("not implemented")

    def update(self, options: dict[str, Any]):
        for opt, val in options.items():
            self.set(opt, val)

    def get_options(self) -> list[str]:
        if not self._name or self._name.lower() == "null":
            return [self._invalid_prefix]
        res = [self._prefix, self._name]
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
        self.set("-b:a", f"{bitrate}k")


class VideoCodec(_Codec):
    AVAILABLE_CODECS: dict[str, Self] = {}

    def __init__(self, name: str, valid_options: Iterable[str] | None = None, **kwargs) -> None:
        super().__init__(invalid_prefix="-vn", prefix="-c:v", name=name, valid_options=valid_options, **kwargs)
        self._valid_options.add("-b:v")

    def set_bitrate(self, bitrate: int):
        self.set("-b:v", f"{bitrate}k")


# register AUDIO codecs
AudioCodec.register("null")
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
