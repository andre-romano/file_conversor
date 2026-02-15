
# src\file_conversor\command\text\convert_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.text_backend import TextBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class TextConvertCommand:
    EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = TextBackend.SupportedInFormats
    SupportedOutFormats = TextBackend.SupportedOutFormats

    @classmethod
    def convert(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_suffix=file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            text_backend.convert(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File conversion')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextConvertCommand",
]
