
# src\file_conversor\command\audio\convert_cmd.py

from pathlib import Path
from typing import Callable, override

from file_conversor.backend.audio_video import FFmpegBackend

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

AudioConvertExternalDependencies = FFmpegBackend.EXTERNAL_DEPENDENCIES
AudioConvertInFormats = FFmpegBackend.SupportedInAudioFormats
AudioConvertOutFormats = FFmpegBackend.SupportedOutAudioFormats


class AudioConvertCommand(AbstractCommand[AudioConvertInFormats, AudioConvertOutFormats]):
    input_files: list[Path]
    file_format: AudioConvertOutFormats
    audio_bitrate: int | None
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return AudioConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return AudioConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return AudioConvertOutFormats

    @override
    def execute(self):
        # init ffmpeg
        ffmpeg_backend = FFmpegBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=self.file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]) -> None:
            ffmpeg_backend.set_files(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            ffmpeg_backend.set_audio_codec(bitrate=self.audio_bitrate)

            # display current progress
            ffmpeg_backend.execute(
                progress_callback=lambda p: self.progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('FFMpeg result')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "AudioConvertExternalDependencies",
    "AudioConvertInFormats",
    "AudioConvertOutFormats",
    "AudioConvertCommand",
]
