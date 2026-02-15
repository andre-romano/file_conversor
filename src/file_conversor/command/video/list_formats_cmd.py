
# src\file_conversor\command\video\list_formats_cmd.py

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from file_conversor.backend.audio_video import FFmpegBackend
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoListFormatsCommand:
    EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

    SupportedOutFormats = FFmpegBackend.SupportedOutFormats

    @dataclass
    class AvailableCodecs:
        file_format: str
        video_codecs: Iterable[str]
        audio_codecs: Iterable[str]

    @classmethod
    def list_formats(
        cls,
        desired_format: SupportedOutFormats | None,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> list[AvailableCodecs]:
        logger.info(f"{_('Retrieving available formats and codecs')}...")

        data_list: list[VideoListFormatsCommand.AvailableCodecs] = []
        for idx, format_enum in enumerate(FFmpegBackend.SupportedOutFormats, start=1):
            try:
                container = FFmpegBackend.SupportedOutAudioFormats(format_enum.value).container
            except ValueError:
                container = FFmpegBackend.SupportedOutVideoFormats(format_enum.value).container

            if desired_format is not None and desired_format.value != format_enum.value:
                continue

            data_list.append(VideoListFormatsCommand.AvailableCodecs(
                file_format=format_enum.value,
                video_codecs=[codec.value for codec in container.available_video_codecs],
                audio_codecs=[codec.value for codec in container.available_audio_codecs],
            ))
            progress_callback(100.0 * float(idx) / len(FFmpegBackend.SupportedOutVideoFormats))

        logger.info(f"{_('File info retrieval')}: [bold green]{_('SUCCESS')}[/].")
        return data_list


__all__ = [
    "VideoListFormatsCommand",
]
