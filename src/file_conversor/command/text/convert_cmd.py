
# src\file_conversor\command\text\convert_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.text_backend import TextBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

TextConvertExternalDependencies = TextBackend.EXTERNAL_DEPENDENCIES

TextConvertInFormats = TextBackend.SupportedInFormats
TextConvertOutFormats = TextBackend.SupportedOutFormats


class TextConvertCommand(AbstractCommand[TextConvertInFormats, TextConvertOutFormats]):
    input_files: list[Path]
    file_format: TextConvertOutFormats
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return TextConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return TextConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return TextConvertOutFormats

    @override
    def execute(self):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=self.file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            text_backend.convert(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            self.progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File conversion')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextConvertExternalDependencies",
    "TextConvertInFormats",
    "TextConvertOutFormats",
    "TextConvertCommand",
]
