
# src\file_conversor\command\pdf\encrypt_cmd.py

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


class PdfEncryptCommand:
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = PyPDFBackend.SupportedInFormats

    EncryptionPermission = PyPDFBackend.EncryptionPermission
    EncryptionAlgorithm = PyPDFBackend.EncryptionAlgorithm

    @classmethod
    def encrypt(
        cls,
        input_files: list[Path],
        owner_password: str,
        permissions: list[EncryptionPermission],
        user_password: str,
        decrypt_password: str,
        algorithm: EncryptionAlgorithm,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
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
                owner_password=owner_password,
                user_password=user_password,
                decrypt_password=decrypt_password,

                # permissions
                permissions=permissions,

                encryption_algorithm=algorithm,
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Encryption')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfEncryptCommand",
]
