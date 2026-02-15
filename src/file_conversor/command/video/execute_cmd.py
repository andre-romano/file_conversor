
# src\file_conversor\command\video\execute_cmd.py

from pathlib import Path
from typing import Any, Callable

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel
from file_conversor.command.video._ffmpeg_cmd_helper import FFmpegCmdHelper
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoExecuteCommand:
    EXTERNAL_DEPENDENCIES = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
    SupportedOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

    AudioCodecs = FFmpegCmdHelper.AudioCodecs
    VideoCodecs = FFmpegCmdHelper.VideoCodecs

    VideoProfile = FFmpegCmdHelper.VideoProfile
    VideoEncoding = FFmpegCmdHelper.VideoEncoding
    VideoQuality = FFmpegCmdHelper.VideoQuality

    MirrorAxis = FFmpegCmdHelper.MirrorAxis
    Rotation = FFmpegCmdHelper.Rotation

    @classmethod
    def execute(
        cls,
        input_files: list[Path],
        file_format: SupportedOutFormats,
        audio_bitrate: int | None,
        video_bitrate: int | None,
        audio_codec: AudioCodecs | None,
        video_codec: VideoCodecs | None,
        audio_filters: list[str],
        video_filters: list[str],
        ffmpeg_args: str,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_suffix=file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            datamodel=batch_datamodel,
            progress_callback=progress_callback,
        )

        # set filters
        ffmpeg_cmd_helper.set_audio_filters(custom_filters=audio_filters)
        ffmpeg_cmd_helper.set_video_filters(custom_filters=video_filters)

        ffmpeg_cmd_helper.set_codecs(audio_codec=audio_codec, video_codec=video_codec)
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)

        ffmpeg_cmd_helper.set_ffmpeg_args(ffmpeg_args)

        ffmpeg_cmd_helper.execute()

        logger.info(f"{_('FFMpeg execution')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "VideoExecuteCommand",
]
