
# src\file_conversor\command\pdf\extract_img_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.pdf import PyMuPDFBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfExtractImgCommand:
    EXTERNAL_DEPENDENCIES = PyMuPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyMuPDFBackend.SupportedInFormats
    SupportedOutFormats = PyMuPDFBackend.SupportedOutFormats

    @classmethod
    def extract_img(
        cls,
        input_files: list[Path],
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pymupdf_backend = PyMuPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Extracting images from')} '{data.input_file}' ...")
            pymupdf_backend.extract_images(
                # files
                overwrite_output=data.overwrite_output,
                input_file=data.input_file,
                output_dir=output_dir,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Extract images')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfExtractImgCommand",
]
