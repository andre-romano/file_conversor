
# src\file_conversor\command\audio\info_cmd.py


# user-provided modules

from enum import StrEnum
from pathlib import Path
from typing import override

from file_conversor.backend.audio_video import FFprobeBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.video.info_cmd import VideoInfoCommand, VideoInfoDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

AudioInfoExternalDependencies = FFprobeBackend.EXTERNAL_DEPENDENCIES
AudioInfoInFormats = FFprobeBackend.SupportedInAudioFormats


class AudioInfoOutFormats (StrEnum):
    pass  # no output formats, since this command is only for getting info about the input file, not for converting it.


class AudioInfoCommand(AbstractCommand[AudioInfoInFormats, AudioInfoOutFormats]):
    input_files: list[Path]
    output: list[VideoInfoDataModel] = []

    @classmethod
    @override
    def _external_dependencies(cls):
        return AudioInfoExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return AudioInfoInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return AudioInfoOutFormats

    @override
    def execute(self) -> None:
        """ Reuse the same logic as VideoInfoCommand, since the info extraction is the same for both audio and video files. """
        command = VideoInfoCommand(
            input_files=self.input_files,
            progress_callback=self.progress_callback,
        )
        command.execute()
        self.output = command.output


__all__ = [
    "AudioInfoCommand",
]
