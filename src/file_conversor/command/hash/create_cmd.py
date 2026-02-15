
# src\file_conversor\command\hash\create_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.hash_backend import HashBackend

# user-provided modules
from file_conversor.command.data_models import FilesDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCreateCommand:
    EXTERNAL_DEPENDENCIES = HashBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = HashBackend.SupportedInFormats
    SupportedOutFormats = HashBackend.SupportedOutFormats

    @classmethod
    def create(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        datamodel = FilesDataModel(
            input_files=input_files,
            output_file=output_dir / f"CHECKSUM.{file_format.value}",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        hash_backend = HashBackend(
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def step_one(data: FilesDataModel, get_progress: Callable[[float], float]):
            hash_backend.generate(
                input_files=data.input_files,
                output_file=data.output_file,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        datamodel.execute(step_one)

        logger.info(f"{_('Hash creation')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "HashCreateCommand",
]
