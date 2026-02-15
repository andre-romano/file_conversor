
# src\file_conversor\command\image\convert_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageConvertCommand:
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PillowBackend.SupportedInFormats
    SupportedOutFormats = PillowBackend.SupportedOutFormats

    @classmethod
    def convert(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        quality: int,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_suffix=file_format.value,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.convert(
                input_file=data.input_file,
                output_file=data.output_file,
                quality=quality,
            )
            progress_callback(get_progress(100.0))

        datamodel.execute(step_one)

        logger.info(f"{_('Image convertion')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageConvertCommand",
]
