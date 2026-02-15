
# src\file_conversor\command\image\info_cmd.py

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


class ImageInfoCommand:
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PillowBackend.SupportedInFormats

    Exif = PillowBackend.Exif
    ExifTags = PillowBackend.Exif_TAGS

    @classmethod
    def info(
        cls,
        input_files: list[Path],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=True,
        )

        res: dict[Path, ImageInfoCommand.Exif] = {}

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")

            # 📁 Informações gerais do arquivo
            res[data.input_file] = pillow_backend.info(data.input_file)
            progress_callback(get_progress(100.0))

        datamodel.execute(step_one)

        return res


__all__ = [
    "ImageInfoCommand",
]
