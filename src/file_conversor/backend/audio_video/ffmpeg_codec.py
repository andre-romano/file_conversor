# src\file_conversor\backend\audio_video\codec.py

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
        valid_options: Iterable[str] | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._invalid_prefix = invalid_prefix
        self._prefix = prefix
        self._name = name
        self._options: dict[str, str | int | None] = {}
        self._valid_options = set(valid_options or [])
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

    def set(self, option: str, value: Any = None):
        if option not in self._valid_options:
            logger.warning(f"Option '{option}' {_('not valid for codec')} '{self._name}'. {_('Valid options are:')} {', '.join(self._valid_options)}")
            return
        if option in self._options and value:
            self._options[option] = f"{self._options[option]},{value}"
        else:
            self._options[option] = value

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
            valid_options: Iterable[str] | None = None,
            options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(invalid_prefix="-an", prefix="-c:a", name=name, valid_options=valid_options, options=options)
        self._valid_options.add("-b:a")

    def set_bitrate(self, bitrate: int):
        self.set("-b:a", f"{bitrate}k")

    def set_filters(self, *filters: FFmpegFilter):
        for filter in filters:
            self.set("-af", filter.get())


class FFmpegVideoCodec(_FFmpegCodec):
    _REGISTERED: dict[str, tuple[tuple, dict[str, Any]]] = {}

    def __init__(
            self,
            name: str,
            valid_options: Iterable[str] | None = None,
            options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(invalid_prefix="-vn", prefix="-c:v", name=name, valid_options=valid_options, options=options)
        self._valid_options.add("-b:v")
        self._valid_options.add("-vf")

    def set_bitrate(self, bitrate: int):
        self.set("-b:v", f"{bitrate}k")

    def set_filters(self, *filters: FFmpegFilter):
        for filter in filters:
            self.set("-vf", filter.get())


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

# register VIDEO codecs
FFmpegVideoCodec.register("null", name="null")
FFmpegVideoCodec.register("copy", name="copy")

FFmpegVideoCodec.register("h264_nvenc", name="h264_nvenc",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })
FFmpegVideoCodec.register("hevc_nvenc", name="hevc_nvenc",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })


FFmpegVideoCodec.register("h264_vaapi", name="h264_vaapi",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })
FFmpegVideoCodec.register("hevc_vaapi", name="hevc_vaapi",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })

FFmpegVideoCodec.register("h264_qsv", name="h264_qsv",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })
FFmpegVideoCodec.register("hevc_qsv", name="hevc_qsv",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })

FFmpegVideoCodec.register("libx264", name="libx264",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })
FFmpegVideoCodec.register("libx265", name="libx265",
                          valid_options={
                              "-preset",
                              "-crf",
                              "-profile:v",
                          }, options={
                              "-preset": "medium",
                              "-profile:v": "high",
                          })

FFmpegVideoCodec.register("vp8_vaapi", name="vp8_vaapi")
FFmpegVideoCodec.register("vp9_vaapi", name="vp9_vaapi")

FFmpegVideoCodec.register("vp8_qsv", name="vp8_qsv")
FFmpegVideoCodec.register("vp9_qsv", name="vp9_qsv")

FFmpegVideoCodec.register("av1_nvenc", name="av1_nvenc")
FFmpegVideoCodec.register("av1_vaapi", name="av1_vaapi")
FFmpegVideoCodec.register("av1_qsv", name="av1_qsv")

FFmpegVideoCodec.register("libvpx", name="libvpx")
FFmpegVideoCodec.register("libvpx-vp9", name="libvpx-vp9")
FFmpegVideoCodec.register("libaom-av1", name="libaom-av1")

FFmpegVideoCodec.register("mpeg4", name="mpeg4")
