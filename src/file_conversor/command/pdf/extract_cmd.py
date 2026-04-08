
# src\file_conversor\command\pdf\extract_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PdfExtractExternalDependencies = PyPDFBackend.EXTERNAL_DEPENDENCIES

PdfExtractInFormats = PyPDFBackend.SupportedInFormats
PdfExtractOutFormats = PyPDFBackend.SupportedOutFormats


class PdfExtractCommand(AbstractCommand[PdfExtractInFormats, PdfExtractOutFormats]):
    input_files: list[Path]
    pages: list[int]
    password: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfExtractExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfExtractInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfExtractOutFormats

    @override
    def execute(self):
        """ 
        Extract specific pages from PDF files. 

        :param input_files: List of input PDF files.
        :param pages: List of pages to extract
        :param password: Password for encrypted PDF files.
        :param output_dir: Output directory.
        :param progress_callback: Callback function for progress reporting.
        """
        backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_extracted",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Extracting pages from')} '{data.input_file}' ...")
            backend.extract(
                input_file=data.input_file,
                output_file=data.output_file,
                password=self.password,
                pages=self.pages,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfExtractExternalDependencies",
    "PdfExtractInFormats",
    "PdfExtractOutFormats",
    "PdfExtractCommand",
]
