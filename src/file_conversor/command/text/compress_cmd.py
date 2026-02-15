
# src\file_conversor\command\text\compress_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.text_backend import TextBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class TextCompressCommand:
    EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = TextBackend.SupportedInFormats

    @classmethod
    def compress(
        cls,
        input_files: list[Path],
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_stem=f"_compressed",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            text_backend.minify(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File compression')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextCompressCommand",
]
