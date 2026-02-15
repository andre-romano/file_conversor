
# src\file_conversor\command\doc\convert_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.office import LibreofficeWriterBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class DocConvertCommand:
    EXTERNAL_DEPENDENCIES = LibreofficeWriterBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = LibreofficeWriterBackend.SupportedInFormats
    SupportedOutFormats = LibreofficeWriterBackend.SupportedOutFormats

    @classmethod
    def convert(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_suffix=file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        backend = LibreofficeWriterBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def step_one(datamodel: FileDataModel, get_progress: Callable[[float], float]) -> None:
            # Perform conversion
            backend.convert(
                input_path=datamodel.input_file,
                output_path=datamodel.output_file,
            )
            progress_callback(get_progress(100))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "DocConvertCommand",
]
