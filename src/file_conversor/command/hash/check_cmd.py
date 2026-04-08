
# src\file_conversor\command\hash\check_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.hash_backend import HashBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

HashCheckExternalDependencies = HashBackend.EXTERNAL_DEPENDENCIES
HashCheckInFormats = HashBackend.SupportedInFormats
HashCheckOutFormats = HashBackend.SupportedOutFormats


class HashCheckCommand(AbstractCommand[HashCheckInFormats, HashCheckOutFormats]):
    input_files: list[Path]

    @classmethod
    @override
    def _external_dependencies(cls):
        return HashCheckExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return HashCheckInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return HashCheckOutFormats

    @override
    def execute(self):

        hash_backend = HashBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=True,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Checking file')} '{data.input_file}' ...")
            hash_backend.check(
                input_file=data.input_file,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('Hash check')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "HashCheckExternalDependencies",
    "HashCheckInFormats",
    "HashCheckOutFormats",
    "HashCheckCommand",
]
