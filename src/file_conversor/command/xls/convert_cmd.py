
# src\file_conversor\command\xls\convert_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.office import LibreofficeCalcBackend

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


XlsConvertExternalDependencies = LibreofficeCalcBackend.EXTERNAL_DEPENDENCIES
XlsConvertInFormats = LibreofficeCalcBackend.SupportedInFormats
XlsConvertOutFormats = LibreofficeCalcBackend.SupportedOutFormats


class XlsConvertCommand(AbstractCommand[XlsConvertInFormats, XlsConvertOutFormats]):
    input_files: list[Path]
    file_format: XlsConvertOutFormats
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return XlsConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return XlsConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return XlsConvertOutFormats

    @override
    def execute(self):
        backend = LibreofficeCalcBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=self.file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"[bold]{_('Converting files')}[/] ...")
            # Perform conversion
            backend.convert(
                input_path=data.input_file,
                output_path=data.output_file,
            )
            self.progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "XlsConvertExternalDependencies",
    "XlsConvertInFormats",
    "XlsConvertOutFormats",
    "XlsConvertCommand",
]
