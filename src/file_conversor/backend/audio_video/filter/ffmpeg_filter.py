# src\file_conversor\backend\audio_video\ffmpeg_filter.py


from typing import override

from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.utils.formatters import parse_ffmpeg_filter


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

    @override
    def __hash__(self) -> int:
        return hash(self._name) ^ hash(self._args) ^ hash(frozenset(self._options.items()))

    @override
    def __eq__(self, value: object) -> bool:
        if isinstance(value, FFmpegFilter):
            return (self._name == value._name) and (self._args == value._args) and (self._options == value._options)
        return False

    @override
    def __repr__(self) -> str:
        return self.get()

    @override
    def __str__(self) -> str:
        return f"{self._name}({", ".join(self._args)}{", ".join(f"{k}={v}" for k, v in self._options.items())})"

    def get(self) -> str:
        res = f"{self._name}" + ("=" if (self._args or self._options) else "")
        res += ":".join(self._args) + ("," if self._args and self._options else "")
        res += ":".join(f"{k}={v}" for k, v in self._options.items())
        return res


__all__ = [
    "FFmpegFilter",
]
