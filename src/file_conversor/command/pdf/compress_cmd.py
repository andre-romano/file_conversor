
# src\file_conversor\command\pdf\compress_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.pdf import GhostscriptBackend, PikePDFBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfCompressCommand:
    EXTERNAL_DEPENDENCIES: set[str] = set(
        *GhostscriptBackend.EXTERNAL_DEPENDENCIES,
        *PikePDFBackend.EXTERNAL_DEPENDENCIES,
    )

    SupportedInFormats = GhostscriptBackend.SupportedInFormats

    Compression = GhostscriptBackend.Compression

    @classmethod
    def compress(
        cls,
        input_files: list[Path],
        compression: Compression,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pikepdf_backend = PikePDFBackend(
            verbose=STATE.loglevel.get().is_verbose(),
        )
        gs_backend = GhostscriptBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_compressed"
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ...")
            gs_backend.compress(
                input_file=data.input_file,
                output_file=data.output_file,
                compression_level=compression,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        def step_two(data: FileDataModel, get_progress: Callable[[float], float]):
            pikepdf_backend.compress(
                # files
                input_file=data.input_file,
                output_file=data.output_file,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )
        batch_datamodel.execute(step_one, step_two)
        logger.info(f"{_('File compression')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfCompressCommand",
]
