
# src\file_conversor\command\pdf\extract_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfExtractCommand:
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyPDFBackend.SupportedInFormats

    @classmethod
    def extract(
        cls,
        input_files: list[Path],
        pages: list[int],
        password: str,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
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
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_extracted",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Extracting pages from')} '{data.input_file}' ...")
            backend.extract(
                input_file=data.input_file,
                output_file=data.output_file,
                password=password,
                pages=pages,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfExtractCommand",
]
