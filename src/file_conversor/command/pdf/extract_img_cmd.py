
# src\file_conversor\command\pdf\extract_img_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyMuPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


PdfExtractImgExternalDependencies = PyMuPDFBackend.EXTERNAL_DEPENDENCIES
PdfExtractImgInFormats = PyMuPDFBackend.SupportedInFormats
PdfExtractImgOutFormats = PyMuPDFBackend.SupportedOutFormats


class PdfExtractImgCommand(AbstractCommand[PdfExtractImgInFormats, PdfExtractImgOutFormats]):
    input_files: list[Path]
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfExtractImgExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfExtractImgInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfExtractImgOutFormats

    @override
    def execute(self):
        pymupdf_backend = PyMuPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Extracting images from')} '{data.input_file}' ...")
            pymupdf_backend.extract_images(
                # files
                overwrite_output=data.overwrite_output,
                input_file=data.input_file,
                output_dir=self.output_dir,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Extract images')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfExtractImgExternalDependencies",
    "PdfExtractImgInFormats",
    "PdfExtractImgOutFormats",
    "PdfExtractImgCommand",
]
