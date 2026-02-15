
# src\file_conversor\command\image\rotate_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.image import PillowBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageRotateCommand:
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PillowBackend.SupportedInFormats
    SupportedOutFormats = PillowBackend.SupportedOutFormats

    ResamplingOption = PillowBackend.ResamplingOption

    @classmethod
    def rotate(
        cls,
        input_files: list[Path],
        rotation: int,
        resampling: ResamplingOption,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Rotate image files.

        :param input_files: List of input image files to rotate.
        :param rotation: Rotation in degrees. Valid values are between 0 and 360 (clockwise rotation).
        :param resampling: Resampling method to use when rotating the image.
        :param output_dir: Directory where the rotated image files will be saved.
        :param progress_callback: Optional callback function to report progress. It receives a float between 0 and 100.
        """

        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_rotated",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"Processing '{data.output_file}' ... ")
            pillow_backend.rotate(
                input_file=data.input_file,
                output_file=data.output_file,
                rotate=rotation,
                resampling=resampling,
            )
            progress_callback(get_progress(100.0))

        datamodel.execute(step_one)
        logger.info(f"{_('Image rotation')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageRotateCommand",
]
