
# src\file_conversor\command\image\to_pdf_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.image import Img2PDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import FilesDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


ImageToPdfExternalDependencies = Img2PDFBackend.EXTERNAL_DEPENDENCIES

ImageToPdfInFormats = Img2PDFBackend.SupportedInFormats
ImageToPdfOutFormats = Img2PDFBackend.SupportedOutFormats

ImageToPdfFitMode = Img2PDFBackend.FitMode
ImageToPdfPageLayout = Img2PDFBackend.PageLayout


class ImageToPdfCommand(AbstractCommand[ImageToPdfInFormats, ImageToPdfOutFormats]):
    input_files: list[Path]
    dpi: int
    fit: ImageToPdfFitMode
    page_size: ImageToPdfPageLayout
    set_metadata: bool
    output_file: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return ImageToPdfExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ImageToPdfInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ImageToPdfOutFormats

    @override
    def execute(self):
        img2pdf_backend = Img2PDFBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = FilesDataModel(
            input_files=self.input_files,
            output_file=self.output_file,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FilesDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            img2pdf_backend.to_pdf(
                input_files=data.input_files,
                output_file=data.output_file,
                dpi=self.dpi,
                image_fit=self.fit,
                page_size=self.page_size,
                include_metadata=self.set_metadata,
            )
            self.progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('PDF generation')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageToPdfExternalDependencies",
    "ImageToPdfInFormats",
    "ImageToPdfOutFormats",
    "ImageToPdfFitMode",
    "ImageToPdfPageLayout",
    "ImageToPdfCommand",
]
