
# src\file_conversor\command\doc\convert_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.office import LibreofficeWriterBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import CONFIG, LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

DocConvertExternalDependencies = LibreofficeWriterBackend.EXTERNAL_DEPENDENCIES
DocConvertInFormats = LibreofficeWriterBackend.SupportedInFormats
DocConvertOutFormats = LibreofficeWriterBackend.SupportedOutFormats


class DocConvertCommand(AbstractCommand[DocConvertInFormats, DocConvertOutFormats]):
    input_files: list[Path]
    file_format: DocConvertOutFormats
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return DocConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return DocConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return DocConvertOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=self.file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        backend = LibreofficeWriterBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def step_one(datamodel: FileDataModel, get_progress: Callable[[float], float]) -> None:
            # Perform conversion
            backend.convert(
                input_path=datamodel.input_file,
                output_path=datamodel.output_file,
            )
            self.progress_callback(get_progress(100))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "DocConvertExternalDependencies",
    "DocConvertInFormats",
    "DocConvertOutFormats",
    "DocConvertCommand",
]
