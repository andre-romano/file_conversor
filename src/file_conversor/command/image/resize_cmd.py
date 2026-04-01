
# src\file_conversor\command\image\resize_cmd.py

from pathlib import Path
from typing import Callable, override

from pydantic import model_validator

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

ImageResizeExternalDependencies = PillowBackend.EXTERNAL_DEPENDENCIES

ImageResizeInFormats = PillowBackend.SupportedInFormats
ImageResizeOutFormats = PillowBackend.SupportedOutFormats

ImageResizeResamplingOption = PillowBackend.ResamplingOption


class ImageResizeCommand(AbstractCommand[ImageResizeInFormats, ImageResizeOutFormats]):
    input_files: list[Path]
    scale: float | None
    width: int | None
    resampling: ImageResizeResamplingOption
    output_dir: Path

    @model_validator(mode="after")
    def _check_model(self):
        if self.scale is None and self.width is None:
            raise ValueError(_("Need either scale or width to resize an image"))
        if self.scale is not None and self.scale <= 0:
            raise ValueError(_("Scale must be >0"))
        if self.width is not None and self.width <= 0:
            raise RuntimeError(_("Width must be >0"))
        return self

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageResizeExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageResizeInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageResizeOutFormats

    @override
    def execute(self):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_resized",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.resize(
                input_file=data.input_file,
                output_file=data.output_file,
                scale=self.scale,
                width=self.width,
                resampling=self.resampling,
            )
            self.progress_callback(get_progress(100.0))  # pyright: ignore[reportUnreachable]

        datamodel.execute(step_one)
        logger.info(f"{_('Image resize')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "ImageResizeExternalDependencies",
    "ImageResizeInFormats",
    "ImageResizeOutFormats",
    "ImageResizeResamplingOption",
    "ImageResizeCommand",
]
