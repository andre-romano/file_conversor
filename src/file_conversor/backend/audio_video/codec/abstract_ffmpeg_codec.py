# src\file_conversor\backend\audio_video\codec.py

from typing import Any, Protocol, override

from file_conversor.backend.audio_video.filter.ffmpeg_filter import FFmpegFilter
from file_conversor.config import Log, get_translation


LOG = Log.get_instance()
_ = get_translation()

logger = LOG.getLogger(__name__)


class SetBitrateProtocol(Protocol):
    def set_bitrate(self, bitrate: int):
        """Set bitrate for the codec."""
        ...


class SetFiltersProtocol(Protocol):

    def set_filters(self, *filters: FFmpegFilter):
        """Set filters for the codec."""
        ...


class AbstractFFmpegCodec(SetBitrateProtocol, SetFiltersProtocol):
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
        self._options: dict[str, str | None] = {}
        self._bitrate: int = 0
        self.update(options or {})

    # PROPERTIES
    @property
    def name(self):
        return self._name

    @property
    def bitrate(self) -> int:
        return self._bitrate

    def _set_bitrate(self, option: str, value: int):
        if value < 0:
            logger.warning(f"{_('Unsetting bitrate for codec')} '{self._name}'")
            self.unset(option)
            self._bitrate = 0
            return
        self.set(option, f"{value}k" if value > 0 else "0")
        self._bitrate = value

    def _set_filters(self, option: str, *filters: FFmpegFilter):
        for filter in filters:
            self.add(option, filter.get())

    # DUNDER METHODS
    @override
    def __eq__(self, value: object) -> bool:
        if isinstance(value, AbstractFFmpegCodec):
            return (self._name == value._name)
        return False

    @override
    def __hash__(self) -> int:
        return hash(self._name)

    @override
    def __repr__(self) -> str:
        return f"{self._name} ({' '.join(self.get_options())})"

    @override
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
        self._options[option] = str(value)

    def unset(self, option: str):
        if option in self._options:
            del self._options[option]

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


__all__ = [
    "AbstractFFmpegCodec",
]
