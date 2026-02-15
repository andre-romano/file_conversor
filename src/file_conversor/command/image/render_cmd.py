
# src\file_conversor\command\image\render_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.image import PyMuSVGBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageRenderCommand:
    EXTERNAL_DEPENDENCIES = PyMuSVGBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyMuSVGBackend.SupportedInFormats
    SupportedOutFormats = PyMuSVGBackend.SupportedOutFormats

    @classmethod
    def render(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        dpi: int,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        pymusvg_backend = PyMuSVGBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_suffix=file_format.value,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pymusvg_backend.convert(
                input_file=data.input_file,
                output_file=data.output_file,
                dpi=dpi,
            )
            progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('Image render')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageRenderCommand",
]
