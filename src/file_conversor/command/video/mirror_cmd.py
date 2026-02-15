
# src\file_conversor\command\video\mirror_cmd.py

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


class VideoMirrorCommand:
    EXTERNAL_DEPENDENCIES = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
    SupportedOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

    VideoProfile = FFmpegCmdHelper.VideoProfile
    VideoEncoding = FFmpegCmdHelper.VideoEncoding
    VideoQuality = FFmpegCmdHelper.VideoQuality

    MirrorAxis = FFmpegCmdHelper.MirrorAxis

    @classmethod
    def mirror(
        cls,
        input_files: list[Path],
        mirror_axis: MirrorAxis | None,
        file_format: FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats,
        audio_bitrate: int | None,
        video_bitrate: int | None,
        video_profile: VideoProfile,
        video_encoding_speed: VideoEncoding,
        video_quality: VideoQuality,
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            out_stem="_mirrored",
            out_suffix=file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            datamodel=batch_datamodel,
            progress_callback=progress_callback,
        )

        ffmpeg_cmd_helper.set_video_settings(
            profile=video_profile,
            encoding_speed=video_encoding_speed,
            quality=video_quality,
        )
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)

        ffmpeg_cmd_helper.set_video_filters(
            mirror_axis=mirror_axis,
        )

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoMirrorCommand",
]
