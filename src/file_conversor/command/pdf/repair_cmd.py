
# src\file_conversor\command\pdf\repair_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PikePDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PdfRepairExternalDependencies: set[str] = PikePDFBackend.EXTERNAL_DEPENDENCIES
PdfRepairInFormats = PikePDFBackend.SupportedInFormats
PdfRepairOutFormats = PikePDFBackend.SupportedOutFormats


class PdfRepairCommand(AbstractCommand[PdfRepairInFormats, PdfRepairOutFormats]):
    input_files: list[Path]
    password: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfRepairExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfRepairInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfRepairOutFormats

    @override
    def execute(self):
        pikepdf_backend = PikePDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_repaired",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pikepdf_backend.compress(
                # files
                input_file=data.input_file,
                output_file=data.output_file,

                # options
                decrypt_password=self.password,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Repair PDF')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfRepairExternalDependencies",
    "PdfRepairInFormats",
    "PdfRepairOutFormats",
    "PdfRepairCommand",
]
