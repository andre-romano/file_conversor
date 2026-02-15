
# src\file_conversor\command\video\check_cmd.py

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


class VideoCheckCommand:
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFprobeBackend.SupportedInVideoFormats

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
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Checking file')} '{data.input_file}' ...")
            # display current progress
            try:
                backend.info(data.input_file)
            except Exception as e:
                logger.error(f"{_('Error checking file')} '{data.input_file}': {e}")
            progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File check')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "VideoCheckCommand",
]
