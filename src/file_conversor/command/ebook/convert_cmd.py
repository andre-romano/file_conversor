
# src\file_conversor\command\ebook_commands.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.ebook import CalibreBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import CONFIG, LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


EbookConvertExternalDependencies = CalibreBackend.EXTERNAL_DEPENDENCIES
EbookConvertInFormats = CalibreBackend.SupportedInFormats
EbookConvertOutFormats = CalibreBackend.SupportedOutFormats


class EbookConvertCommand(AbstractCommand[EbookConvertInFormats, EbookConvertOutFormats]):
    input_files: list[Path]
    file_format: EbookConvertOutFormats
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return EbookConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return EbookConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return EbookConvertOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=self.file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        calibre_backend = CalibreBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            calibre_backend.convert(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            self.progress_callback(get_progress(100))

        batch_datamodel.execute(step_one)

        logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "EbookConvertExternalDependencies",
    "EbookConvertInFormats",
    "EbookConvertOutFormats",
    "EbookConvertCommand",
]
