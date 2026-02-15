
# src\file_conversor\command\pdf\merge_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.data_models import FilesDataModel
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.utils.formatters import get_output_file


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfMergeCommand:
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyPDFBackend.SupportedInFormats
    SupportedOutFormats = PyPDFBackend.SupportedOutFormats

    @classmethod
    def merge(
        cls,
        input_files: list[Path],
        password: str,
        output_file: Path | None,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = FilesDataModel(
            input_files=input_files,
            output_file=output_file if output_file else get_output_file(
                input_files[0],
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
                password=password,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfMergeCommand",
]
