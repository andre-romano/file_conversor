
# src\file_conversor\command\audio\info_cmd.py


# user-provided modules

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.audio_video import FFprobeBackend
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioInfoCommand:
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFprobeBackend.SupportedInAudioFormats

    @classmethod
    def info(
        cls,
        input_files: list[Path],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        """ Reuse the same logic as VideoInfoCommand, since the info extraction is the same for both audio and video files. """
        raise NotImplementedError("AudioInfoCommand.info is not implemented. Use VideoInfoCommand.info .")


__all__ = [
    "AudioInfoCommand",
]
