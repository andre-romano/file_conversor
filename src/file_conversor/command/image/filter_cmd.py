
# src\file_conversor\command\image\filter_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

ImageFilterExternalDependencies = PillowBackend.EXTERNAL_DEPENDENCIES
ImageFilterInFormats = PillowBackend.SupportedInFormats
ImageFilterOutFormats = PillowBackend.SupportedOutFormats

ImageFilterFilters = PillowBackend.PillowFilter


class ImageFilterCommand(AbstractCommand[ImageFilterInFormats, ImageFilterOutFormats]):
    input_files: list[Path]
    filters: list[ImageFilterFilters]
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageFilterExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageFilterInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageFilterOutFormats

    @override
    def execute(self):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_filtered",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.filter(
                input_file=data.input_file,
                output_file=data.output_file,
                filters=self.filters,
            )
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('Image filter')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageFilterExternalDependencies",
    "ImageFilterInFormats",
    "ImageFilterOutFormats",
    "ImageFilterFilters",
    "ImageFilterCommand",
]
