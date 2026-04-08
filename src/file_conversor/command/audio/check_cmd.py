
# src\file_conversor\command\audio\check.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.audio_video import FFprobeBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import CONFIG, LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

AudioCheckExternalDependencies = FFprobeBackend.EXTERNAL_DEPENDENCIES
AudioCheckInFormats = FFprobeBackend.SupportedInAudioFormats
AudioCheckOutFormats = FFprobeBackend.SupportedOutAudioFormats


class AudioCheckCommand(AbstractCommand[AudioCheckInFormats, AudioCheckOutFormats]):
    input_files: list[Path]

    @classmethod
    @override
    def _external_dependencies(cls):
        return AudioCheckExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return AudioCheckInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return AudioCheckOutFormats

    @override
    def execute(self):
        backend = FFprobeBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=True,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]) -> None:
            try:
                backend.info(data.input_file)
                self.progress_callback(get_progress(100.0))
            except Exception as e:
                logger.error(f"{_('Error checking file')} '{data.input_file}': {e}")

        batch_datamodel.execute(step_one)
        logger.info(f"{_('FFMpeg check')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "AudioCheckCommand",
]
