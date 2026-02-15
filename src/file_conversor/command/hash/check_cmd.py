
# src\file_conversor\command\hash\check_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.hash_backend import HashBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCheckCommand:
    EXTERNAL_DEPENDENCIES = HashBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = HashBackend.SupportedInFormats
    SupportedOutFormats = HashBackend.SupportedOutFormats

    @classmethod
    def check(
        cls,
        input_files: list[Path],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):

        hash_backend = HashBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=True,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Checking file')} '{data.input_file}' ...")
            hash_backend.check(
                input_file=data.input_file,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Hash check')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "HashCheckCommand",
]
