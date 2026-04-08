
# src\file_conversor\command\image\mirror_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


ImageMirrorExternalDependencies = PillowBackend.EXTERNAL_DEPENDENCIES

ImageMirrorInFormats = PillowBackend.SupportedInFormats
ImageMirrorOutFormats = PillowBackend.SupportedOutFormats

ImageMirrorAxis = PillowBackend.MirrorAxis


class ImageMirrorCommand(AbstractCommand[ImageMirrorInFormats, ImageMirrorOutFormats]):
    input_files: list[Path]
    axis: ImageMirrorAxis
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageMirrorExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageMirrorInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageMirrorOutFormats

    @override
    def execute(self):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_mirrored",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.mirror(
                input_file=data.input_file,
                output_file=data.output_file,
                axis=self.axis,
            )
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('Image mirroring')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageMirrorExternalDependencies",
    "ImageMirrorInFormats",
    "ImageMirrorOutFormats",
    "ImageMirrorAxis",
    "ImageMirrorCommand",
]
