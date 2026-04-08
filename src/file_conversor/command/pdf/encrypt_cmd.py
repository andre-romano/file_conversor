
# src\file_conversor\command\pdf\encrypt_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import PyPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PdfEncryptExternalDependencies = PyPDFBackend.EXTERNAL_DEPENDENCIES

PdfEncryptInFormats = PyPDFBackend.SupportedInFormats
PdfEncryptOutFormats = PyPDFBackend.SupportedOutFormats

PdfEncryptPermission = PyPDFBackend.EncryptionPermission
PdfEncryptAlgorithm = PyPDFBackend.EncryptionAlgorithm


class PdfEncryptCommand(AbstractCommand[PdfEncryptInFormats, PdfEncryptOutFormats]):
    input_files: list[Path]
    owner_password: str
    permissions: list[PdfEncryptPermission]
    user_password: str
    decrypt_password: str
    algorithm: PdfEncryptAlgorithm
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfEncryptExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfEncryptInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfEncryptOutFormats

    @override
    def execute(self):
        backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_encrypted",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Encrypting file')} '{data.input_file}' ...")
            backend.encrypt(
                # files
                input_file=data.input_file,
                output_file=data.output_file,
                # passwords
                owner_password=self.owner_password,
                user_password=self.user_password,
                decrypt_password=self.decrypt_password,

                # permissions
                permissions=self.permissions,

                encryption_algorithm=self.algorithm,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Encryption')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfEncryptExternalDependencies",
    "PdfEncryptInFormats",
    "PdfEncryptOutFormats",
    "PdfEncryptPermission",
    "PdfEncryptAlgorithm",
    "PdfEncryptCommand",
]
