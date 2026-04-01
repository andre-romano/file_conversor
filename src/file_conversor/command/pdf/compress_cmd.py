
# src\file_conversor\command\pdf\compress_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import GhostscriptBackend, PikePDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


PdfCompressExternalDependencies: set[str] = set(
    *GhostscriptBackend.EXTERNAL_DEPENDENCIES,
    *PikePDFBackend.EXTERNAL_DEPENDENCIES,
)

PdfCompressInFormats = GhostscriptBackend.SupportedInFormats
PdfCompressOutFormats = GhostscriptBackend.SupportedOutFormats

PdfCompressCompression = GhostscriptBackend.Compression


class PdfCompressCommand(AbstractCommand[PdfCompressInFormats, PdfCompressOutFormats]):
    input_files: list[Path]
    compression: PdfCompressCompression
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfCompressExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfCompressInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfCompressOutFormats

    @override
    def execute(self):
        pikepdf_backend = PikePDFBackend(
            verbose=STATE.loglevel.get().is_verbose(),
        )
        gs_backend = GhostscriptBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_compressed"
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ...")
            gs_backend.compress(
                input_file=data.input_file,
                output_file=data.output_file,
                compression_level=self.compression,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        def step_two(data: FileDataModel, get_progress: Callable[[float], float]):
            pikepdf_backend.compress(
                # files
                input_file=data.input_file,
                output_file=data.output_file,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )
        batch_datamodel.execute(step_one, step_two)
        logger.info(f"{_('File compression')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfCompressExternalDependencies",
    "PdfCompressInFormats",
    "PdfCompressOutFormats",
    "PdfCompressCompression",
    "PdfCompressCommand",
]
