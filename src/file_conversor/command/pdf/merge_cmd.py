
# src\file_conversor\command\pdf\merge_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import FilesDataModel
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.utils.formatters import get_output_file


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


PdfMergeExternalDependencies = PyPDFBackend.EXTERNAL_DEPENDENCIES

PdfMergeInFormats = PyPDFBackend.SupportedInFormats
PdfMergeOutFormats = PyPDFBackend.SupportedOutFormats


class PdfMergeCommand(AbstractCommand[PdfMergeInFormats, PdfMergeOutFormats]):
    input_files: list[Path]
    password: str
    output_file: Path | None

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfMergeExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfMergeInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfMergeOutFormats

    @override
    def execute(self):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = FilesDataModel(
            input_files=self.input_files,
            output_file=self.output_file if self.output_file else get_output_file(
                self.input_files[0],
                out_stem="_merged",
            ),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FilesDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ...")
            pypdf_backend.merge(
                # files
                input_files=data.input_files,
                output_file=data.output_file,
                password=self.password,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfMergeExternalDependencies",
    "PdfMergeInFormats",
    "PdfMergeOutFormats",
    "PdfMergeCommand",
]
