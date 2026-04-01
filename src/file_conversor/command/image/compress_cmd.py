
# src\file_conversor\command\image\compress_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import CompressBackend

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

ImageCompressExternalDependencies = CompressBackend.EXTERNAL_DEPENDENCIES
ImageCompressInFormats = CompressBackend.SupportedInFormats
ImageCompressOutFormats = CompressBackend.SupportedOutFormats


class ImageCompressCommand(AbstractCommand[ImageCompressInFormats, ImageCompressOutFormats]):
    input_files: list[Path]
    quality: int
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageCompressExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageCompressInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageCompressOutFormats

    @override
    def execute(self):
        compress_backend = CompressBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_compressed",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            compress_backend.compress(
                input_file=data.input_file,
                output_file=data.output_file,
                quality=self.quality,
            )
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)

        logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageCompressCommand",
]
