
# src\file_conversor\command\image\info_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

ImageInfoExternalDependencies = PillowBackend.EXTERNAL_DEPENDENCIES
ImageInfoInFormats = PillowBackend.SupportedInFormats
ImageInfoOutFormats = PillowBackend.SupportedOutFormats

ImageInfoExifParsed = PillowBackend.ExifParsed


class ImageInfoCommand(AbstractCommand[ImageInfoInFormats, ImageInfoOutFormats]):
    input_files: list[Path]
    output: dict[Path, ImageInfoExifParsed] = {}

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageInfoExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageInfoInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageInfoOutFormats

    @override
    def execute(self):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=True,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")

            # 📁 Informações gerais do arquivo
            self.output[data.input_file] = pillow_backend.info(data.input_file)
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)


__all__ = [
    "ImageInfoExternalDependencies",
    "ImageInfoInFormats",
    "ImageInfoOutFormats",
    "ImageInfoExifParsed",
    "ImageInfoCommand",
]
