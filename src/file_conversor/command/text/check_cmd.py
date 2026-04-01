
# src\file_conversor\command\text\check_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.text_backend import TextBackend

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


TextCheckExternalDependencies = TextBackend.EXTERNAL_DEPENDENCIES
TextCheckInFormats = TextBackend.SupportedInFormats
TextCheckOutFormats = TextBackend.SupportedOutFormats


class TextCheckCommand(AbstractCommand[TextCheckInFormats, TextCheckOutFormats]):
    input_files: list[Path]

    @classmethod
    @override
    def _external_dependencies(cls):
        return TextCheckExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return TextCheckInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return TextCheckOutFormats

    @override
    def execute(self):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Checking file')} '{data.input_file}' ...")
            text_backend.check(
                input_file=data.input_file,
            )
            self.progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File check')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextCheckExternalDependencies",
    "TextCheckInFormats",
    "TextCheckOutFormats",
    "TextCheckCommand",
]
