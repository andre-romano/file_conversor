
# src\file_conversor\command\video\list_formats_cmd.py

from dataclasses import dataclass
from typing import Iterable, override

from file_conversor.backend.audio_video import FFmpegBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


VideoListFormatsExternalDependencies = FFmpegBackend.EXTERNAL_DEPENDENCIES

VideoListFormatsInFormats = FFmpegBackend.SupportedInFormats
VideoListFormatsOutFormats = FFmpegBackend.SupportedOutFormats


@dataclass
class VideoListFormatsAvailableCodecs:
    file_format: str
    video_codecs: Iterable[str]
    audio_codecs: Iterable[str]


class VideoListFormatsCommand(AbstractCommand[VideoListFormatsInFormats, VideoListFormatsOutFormats]):
    desired_format: VideoListFormatsOutFormats | None
    output: list[VideoListFormatsAvailableCodecs] = []

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoListFormatsExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoListFormatsInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoListFormatsOutFormats

    @override
    def execute(self):
        logger.info(f"{_('Retrieving available formats and codecs')}...")

        for idx, format_enum in enumerate(FFmpegBackend.SupportedOutFormats, start=1):
            try:
                container = FFmpegBackend.SupportedOutAudioFormats(format_enum.value).container
            except ValueError:
                container = FFmpegBackend.SupportedOutVideoFormats(format_enum.value).container

            if self.desired_format is not None and self.desired_format.value != format_enum.value:
                continue

            self.output.append(VideoListFormatsAvailableCodecs(
                file_format=format_enum.value,
                video_codecs=[codec.value for codec in container.available_video_codecs],
                audio_codecs=[codec.value for codec in container.available_audio_codecs],
            ))
            self.progress_callback(100.0 * float(idx) / len(FFmpegBackend.SupportedOutVideoFormats))

        logger.info(f"{_('File info retrieval')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "VideoListFormatsExternalDependencies",
    "VideoListFormatsInFormats",
    "VideoListFormatsOutFormats",
    "VideoListFormatsAvailableCodecs",
    "VideoListFormatsCommand",
]
