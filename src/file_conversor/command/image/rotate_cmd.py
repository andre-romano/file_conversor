
# src\file_conversor\command\image\rotate_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


ImageRotateExternalDependencies = PillowBackend.EXTERNAL_DEPENDENCIES

ImageRotateInFormats = PillowBackend.SupportedInFormats
ImageRotateOutFormats = PillowBackend.SupportedOutFormats

ImageRotateResamplingOption = PillowBackend.ResamplingOption


class ImageRotateCommand(AbstractCommand[ImageRotateInFormats, ImageRotateOutFormats]):
    input_files: list[Path]
    rotation: int
    resampling: ImageRotateResamplingOption
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageRotateExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageRotateInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageRotateOutFormats

    @override
    def execute(self):
        """
        Rotate image files.
        """

        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_rotated",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.rotate(
                input_file=data.input_file,
                output_file=data.output_file,
                rotate=self.rotation,
                resampling=self.resampling,
            )
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('Image rotation')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageRotateExternalDependencies",
    "ImageRotateInFormats",
    "ImageRotateOutFormats",
    "ImageRotateResamplingOption",
    "ImageRotateCommand",
]
