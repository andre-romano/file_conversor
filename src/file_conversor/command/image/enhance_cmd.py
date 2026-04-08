
# src\file_conversor\command\image\enhance_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


ImageEnhanceExternalDependencies = PillowBackend.EXTERNAL_DEPENDENCIES
ImageEnhanceInFormats = PillowBackend.SupportedInFormats
ImageEnhanceOutFormats = PillowBackend.SupportedOutFormats


class ImageEnhanceCommand(AbstractCommand[ImageEnhanceInFormats, ImageEnhanceOutFormats]):
    input_files: list[Path]

    brightness: float
    contrast: float
    color: float
    sharpness: float

    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageEnhanceExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageEnhanceInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageEnhanceOutFormats

    @override
    def execute(self):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_enhanced",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.enhance(
                input_file=data.input_file,
                output_file=data.output_file,
                color_factor=self.color,
                brightness_factor=self.brightness,
                contrast_factor=self.contrast,
                sharpness_factor=self.sharpness,
            )
            self.progress_callback(get_progress(100.0))
        datamodel.execute(step_one)

        logger.info(f"{_('Image enhance')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageEnhanceExternalDependencies",
    "ImageEnhanceInFormats",
    "ImageEnhanceOutFormats",
    "ImageEnhanceCommand",
]
