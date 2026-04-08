
# src\file_conversor\command\text\compress_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.text_backend import TextBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


TextCompressExternalDependencies = TextBackend.EXTERNAL_DEPENDENCIES

TextCompressInFormats = TextBackend.SupportedInFormats
TextCompressOutFormats = TextBackend.SupportedOutFormats


class TextCompressCommand(AbstractCommand[TextCompressInFormats, TextCompressOutFormats]):
    input_files: list[Path]
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return TextCompressExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return TextCompressInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return TextCompressOutFormats

    @override
    def execute(self):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem=f"_compressed",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            text_backend.minify(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            self.progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File compression')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextCompressExternalDependencies",
    "TextCompressInFormats",
    "TextCompressOutFormats",
    "TextCompressCommand",
]
