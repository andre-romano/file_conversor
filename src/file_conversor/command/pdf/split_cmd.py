
# src\file_conversor\command\pdf\split_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PdfSplitExternalDependencies = PyPDFBackend.EXTERNAL_DEPENDENCIES
PdfSplitInFormats = PyPDFBackend.SupportedInFormats
PdfSplitOutFormats = PyPDFBackend.SupportedOutFormats


class PdfSplitCommand(AbstractCommand[PdfSplitInFormats, PdfSplitOutFormats]):
    input_files: list[Path]
    password: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfSplitExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfSplitInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfSplitOutFormats

    @override
    def execute(self):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pypdf_backend.split(
                overwrite_output=data.overwrite_output,
                input_file=data.input_file,
                password=self.password,
                out_dir=data.output_file.parent,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfSplitExternalDependencies",
    "PdfSplitInFormats",
    "PdfSplitOutFormats",
    "PdfSplitCommand",
]
