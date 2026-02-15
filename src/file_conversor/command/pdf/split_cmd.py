
# src\file_conversor\command\pdf\split_cmd.py

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


class PdfSplitCommand:
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyPDFBackend.SupportedInFormats
    SupportedOutFormats = PyPDFBackend.SupportedOutFormats

    @classmethod
    def split(
        cls,
        input_files: list[Path],
        password: str,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pypdf_backend.split(
                overwrite_output=data.overwrite_output,
                input_file=data.input_file,
                password=password,
                out_dir=data.output_file.parent,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfSplitCommand",
]
