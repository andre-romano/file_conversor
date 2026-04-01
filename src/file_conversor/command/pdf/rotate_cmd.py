
# src\file_conversor\command\pdf\rotate_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyPDFBackend

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

PdfRotateExternalDependencies = PyPDFBackend.EXTERNAL_DEPENDENCIES
PdfRotateInFormats = PyPDFBackend.SupportedInFormats
PdfRotateOutFormats = PyPDFBackend.SupportedOutFormats

PdfRotateRotation = PyPDFBackend.Rotation


class PdfRotateCommand(AbstractCommand[PdfRotateInFormats, PdfRotateOutFormats]):
    input_files: list[Path]
    rotation: dict[int, PdfRotateRotation]
    password: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfRotateExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfRotateInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfRotateOutFormats

    @classmethod
    def len(cls, input_file: Path) -> int:
        backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())
        return backend.len(input_file)

    @override
    def execute(self):
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
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_rotated",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Processing file')} '{data.input_file}' ...")
            backend.rotate(
                input_file=data.input_file,
                output_file=data.output_file,
                decrypt_password=self.password,
                rotations=self.rotation,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfRotateExternalDependencies",
    "PdfRotateInFormats",
    "PdfRotateOutFormats",
    "PdfRotateRotation",
    "PdfRotateCommand",
]
