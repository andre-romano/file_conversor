
# src\file_conversor\command\image\to_pdf_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.image import Img2PDFBackend

# user-provided modules
from file_conversor.command.data_models import FilesDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageToPdfCommand:
    EXTERNAL_DEPENDENCIES = Img2PDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = Img2PDFBackend.SupportedInFormats
    SupportedOutFormats = Img2PDFBackend.SupportedOutFormats

    FitMode = Img2PDFBackend.FitMode
    PageLayout = Img2PDFBackend.PageLayout

    @classmethod
    def to_pdf(
        cls,
        input_files: list[Path],
        dpi: int,
        fit: FitMode,
        page_size: PageLayout,
        set_metadata: bool,
        output_file: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        img2pdf_backend = Img2PDFBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = FilesDataModel(
            input_files=input_files,
            output_file=output_file,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FilesDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            img2pdf_backend.to_pdf(
                input_files=data.input_files,
                output_file=data.output_file,
                dpi=dpi,
                image_fit=fit,
                page_size=page_size,
                include_metadata=set_metadata,
            )
            progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('PDF generation')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageToPdfCommand",
]
