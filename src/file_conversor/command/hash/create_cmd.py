
# src\file_conversor\command\hash\create_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.hash_backend import HashBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import FilesDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

HashCreateExternalDependencies = HashBackend.EXTERNAL_DEPENDENCIES
HashCreateInFormats = HashBackend.SupportedInFormats
HashCreateOutFormats = HashBackend.SupportedOutFormats


class HashCreateCommand(AbstractCommand[HashCreateInFormats, HashCreateOutFormats]):
    input_files: list[Path]
    file_format: HashCreateOutFormats
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return HashCreateExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return HashCreateInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return HashCreateOutFormats

    @override
    def execute(self):
        datamodel = FilesDataModel(
            input_files=self.input_files,
            output_file=self.output_dir / f"CHECKSUM.{self.file_format.value}",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        hash_backend = HashBackend(
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def step_one(data: FilesDataModel, get_progress: Callable[[float], float]):
            hash_backend.generate(
                input_files=data.input_files,
                output_file=data.output_file,
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        datamodel.execute(step_one)

        logger.info(f"{_('Hash creation')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "HashCreateExternalDependencies",
    "HashCreateInFormats",
    "HashCreateOutFormats",
    "HashCreateCommand",
]
