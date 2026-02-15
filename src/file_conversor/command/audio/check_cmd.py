
# src\file_conversor\command\audio\check.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.audio_video import FFprobeBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioCheckCommand:
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFprobeBackend.SupportedInAudioFormats

    @classmethod
    def check(
        cls,
        input_files: list[Path],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        backend = FFprobeBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=True,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]) -> None:
            try:
                backend.info(data.input_file)
                progress_callback(get_progress(100.0))
            except Exception as e:
                logger.error(f"{_('Error checking file')} '{data.input_file}': {e}")

        batch_datamodel.execute(step_one)
        logger.info(f"{_('FFMpeg check')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "AudioCheckCommand",
]
