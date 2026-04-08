
# src\file_conversor\command\image\render_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import PyMuSVGBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


ImageRenderExternalDependencies = PyMuSVGBackend.EXTERNAL_DEPENDENCIES
ImageRenderInFormats = PyMuSVGBackend.SupportedInFormats
ImageRenderOutFormats = PyMuSVGBackend.SupportedOutFormats


class ImageRenderCommand(AbstractCommand[ImageRenderInFormats, ImageRenderOutFormats]):
    input_files: list[Path]
    file_format: ImageRenderOutFormats
    dpi: int
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageRenderExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageRenderInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageRenderOutFormats

    @override
    def execute(self):
        pymusvg_backend = PyMuSVGBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_suffix=self.file_format.value,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pymusvg_backend.convert(
                input_file=data.input_file,
                output_file=data.output_file,
                dpi=self.dpi,
            )
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('Image render')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageRenderExternalDependencies",
    "ImageRenderInFormats",
    "ImageRenderOutFormats",
    "ImageRenderCommand",
]
