
# src\file_conversor\command\pdf\rotate_cmd.py

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


class PdfRotateCommand:
    EXTERNAL_DEPENDENCIES: set[str] = PyPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyPDFBackend.SupportedInFormats
    SupportedOutFormats = PyPDFBackend.SupportedOutFormats

    @classmethod
    def len(cls, input_file: Path) -> int:
        backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())
        return backend.len(input_file)

    Rotation = PyPDFBackend.Rotation

    @classmethod
    def rotate(
        cls,
        input_files: list[Path],
        rotation: dict[int, Rotation],
        password: str,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Rotate PDF pages.

        :param input_files: List of input PDF files.
        :param rotation: List of rotation instructions, format "page:rotation" or "start-end:rotation" or "start-:rotation".
        :param password: Password to decrypt the PDF if it is encrypted.
        :param output_dir: Directory to save the rotated PDF files.
        :param progress_callback: Callback function to report progress.
        """
        backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_rotated",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Processing file')} '{data.input_file}' ...")
            backend.rotate(
                input_file=data.input_file,
                output_file=data.output_file,
                decrypt_password=password,
                rotations=rotation,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfRotateCommand",
]
