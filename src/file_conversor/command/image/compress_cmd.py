
# src\file_conversor\command\image\compress_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.image import CompressBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageCompressCommand:
    EXTERNAL_DEPENDENCIES = CompressBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = CompressBackend.SupportedInFormats
    SupportedOutFormats = CompressBackend.SupportedOutFormats

    @classmethod
    def compress(
        cls,
        input_files: list[Path],
        quality: int,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        compress_backend = CompressBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_compressed",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            compress_backend.compress(
                input_file=data.input_file,
                output_file=data.output_file,
                quality=quality,
            )
            progress_callback(get_progress(100.0))

        datamodel.execute(step_one)

        logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageCompressCommand",
]
