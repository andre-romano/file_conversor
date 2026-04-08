
# src\file_conversor\command\pdf\decrypt_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PdfDecryptExternalDependencies = PyPDFBackend.EXTERNAL_DEPENDENCIES
PdfDecryptInFormats = PyPDFBackend.SupportedInFormats
PdfDecryptOutFormats = PyPDFBackend.SupportedOutFormats


class PdfDecryptCommand(AbstractCommand[PdfDecryptInFormats, PdfDecryptOutFormats]):
    input_files: list[Path]
    password: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfDecryptExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfDecryptInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfDecryptOutFormats

    @override
    def execute(self):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_decrypted",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Decrypting file')} '{data.input_file}' ...")
            pypdf_backend.decrypt(
                input_file=data.input_file,
                output_file=data.output_file,
                password=self.password,
                progress_callback=lambda p: self.progress_callback(get_progress(p))
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Decryption')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfDecryptExternalDependencies",
    "PdfDecryptInFormats",
    "PdfDecryptOutFormats",
    "PdfDecryptCommand",
]
