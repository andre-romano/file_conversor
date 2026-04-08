
# src\file_conversor\command\pdf\convert_cmd.py

from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, override

from file_conversor.backend.pdf import PDF2DOCXBackend, PyMuPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PdfConvertExternalDependencies: set[str] = set(
    *PyMuPDFBackend.EXTERNAL_DEPENDENCIES,
    *PDF2DOCXBackend.EXTERNAL_DEPENDENCIES,
)

PdfConvertInFormats = PyMuPDFBackend.SupportedInFormats


class PdfConvertOutFormats(StrEnum):
    PNG = PyMuPDFBackend.SupportedOutFormats.PNG.value
    JPG = PyMuPDFBackend.SupportedOutFormats.JPG.value
    DOCX = PDF2DOCXBackend.SupportedOutFormats.DOCX.value


class PdfConvertCommand(AbstractCommand[PdfConvertInFormats, PdfConvertOutFormats]):
    input_files: list[Path]
    file_format: PdfConvertOutFormats
    dpi: int
    password: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfConvertOutFormats

    @override
    def execute(self):
        step_one: Callable[[FileDataModel, Callable[[float], float]], Any]
        try:
            # try to use PyMuPDF for conversion, if the output format is supported by it
            out_format = PyMuPDFBackend.SupportedOutFormats(self.file_format.value)

            backend = PyMuPDFBackend(verbose=STATE.loglevel.get().is_verbose())

            def step_one_mupdf(data: FileDataModel, get_progress: Callable[[float], float]):
                logger.info(f"[bold]{_('Converting file')}[/] '{data.input_file}' {_('with PyMuPDF backend')}...")
                backend.convert(
                    input_file=data.input_file,
                    output_file=data.output_file,
                    dpi=self.dpi,
                    password=self.password,
                )
                self.progress_callback(get_progress(100.0))  # pyright: ignore[reportUnreachable]
            step_one = step_one_mupdf
        except ValueError:
            # try pdf2docx for conversion, if the output format is supported by it
            out_format = PDF2DOCXBackend.SupportedOutFormats(self.file_format.value)

            backend = PDF2DOCXBackend(verbose=STATE.loglevel.get().is_verbose())

            def step_one_pdf2docx(data: FileDataModel, get_progress: Callable[[float], float]):
                logger.info(f"[bold]{_('Converting file')}[/] '{data.input_file}' {_('with PDF2DOCX backend')}...")
                backend.convert(
                    input_file=data.input_file,
                    output_file=data.output_file,
                    password=self.password,
                )
                self.progress_callback(get_progress(100.0))
            step_one = step_one_pdf2docx

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=out_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfConvertExternalDependencies",
    "PdfConvertInFormats",
    "PdfConvertOutFormats",
    "PdfConvertCommand",
]
