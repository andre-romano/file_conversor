
# src\file_conversor\command\audio\convert_cmd.py

from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.audio_video import FFmpegBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioConvertCommand:
    EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFmpegBackend.SupportedInFormats
    SupportedOutFormats = FFmpegBackend.SupportedOutAudioFormats

    @classmethod
    def convert(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        audio_bitrate: int | None,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        # init ffmpeg
        ffmpeg_backend = FFmpegBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_suffix=file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]) -> None:
            ffmpeg_backend.set_files(
                input_file=data.input_file,
                output_file=data.output_file,
            )
            ffmpeg_backend.set_audio_codec(bitrate=audio_bitrate)

            # display current progress
            ffmpeg_backend.execute(
                progress_callback=lambda p: progress_callback(get_progress(p)),
            )

        batch_datamodel.execute(step_one)
        logger.info(f"{_('FFMpeg result')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "AudioConvertCommand",
]
