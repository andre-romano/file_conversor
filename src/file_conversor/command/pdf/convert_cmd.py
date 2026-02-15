
# src\file_conversor\command\pdf\convert_cmd.py

from enum import Enum
from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.pdf import PDF2DOCXBackend, PyMuPDFBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfConvertCommand:
    EXTERNAL_DEPENDENCIES: set[str] = set(
        *PyMuPDFBackend.EXTERNAL_DEPENDENCIES,
        *PDF2DOCXBackend.EXTERNAL_DEPENDENCIES,
    )

    SupportedInFormats = PyMuPDFBackend.SupportedInFormats

    class SupportedOutFormats(Enum):
        PNG = PyMuPDFBackend.SupportedOutFormats.PNG.value
        JPG = PyMuPDFBackend.SupportedOutFormats.JPG.value
        DOCX = PDF2DOCXBackend.SupportedOutFormats.DOCX.value

    @classmethod
    def convert(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        dpi: int,
        password: str,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        step_one: Callable[[FileDataModel, Callable[[float], float]], Any]
        try:
            # try to use PyMuPDF for conversion, if the output format is supported by it
            out_format = PyMuPDFBackend.SupportedOutFormats(file_format.value)

            backend = PyMuPDFBackend(verbose=STATE.loglevel.get().is_verbose())

            def step_one_mupdf(data: FileDataModel, get_progress: Callable[[float], float]):
                logger.info(f"[bold]{_('Converting file')}[/] '{data.input_file}' {_('with PyMuPDF backend')}...")
                backend.convert(
                    input_file=data.input_file,
                    output_file=data.output_file,
                    dpi=dpi,
                    password=password,
                )
                progress_callback(get_progress(100.0))  # pyright: ignore[reportUnreachable]
            step_one = step_one_mupdf
        except ValueError:
            # try pdf2docx for conversion, if the output format is supported by it
            out_format = PDF2DOCXBackend.SupportedOutFormats(file_format.value)

            backend = PDF2DOCXBackend(verbose=STATE.loglevel.get().is_verbose())

            def step_one_pdf2docx(data: FileDataModel, get_progress: Callable[[float], float]):
                logger.info(f"[bold]{_('Converting file')}[/] '{data.input_file}' {_('with PDF2DOCX backend')}...")
                backend.convert(
                    input_file=data.input_file,
                    output_file=data.output_file,
                    password=password,
                )
                progress_callback(get_progress(100.0))
            step_one = step_one_pdf2docx

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_suffix=out_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfConvertCommand",
]
