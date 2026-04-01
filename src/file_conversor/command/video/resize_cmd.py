
# src\file_conversor\command\video\resize_cmd.py

from pathlib import Path
from typing import override

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel
from file_conversor.command.video._ffmpeg_cmd_helper import FFmpegCmdHelper
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


VideoResizeExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

VideoResizeInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoResizeOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoResizeProfile = FFmpegCmdHelper.VideoProfile
VideoResizeEncoding = FFmpegCmdHelper.VideoEncoding
VideoResizeQuality = FFmpegCmdHelper.VideoQuality


class VideoResizeCommand(AbstractCommand[VideoResizeInFormats, VideoResizeOutFormats]):
    input_files: list[Path]
    resolution: tuple[int, int] | None
    file_format: VideoResizeOutFormats
    audio_bitrate: int | None
    video_bitrate: int | None
    video_profile: VideoResizeProfile
    video_encoding_speed: VideoResizeEncoding
    video_quality: VideoResizeQuality
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoResizeExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoResizeInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoResizeOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem="_resized",
            out_suffix=self.file_format.value,
            overwrite_output=STATE.overwrite_output.enabled,
        )

        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            datamodel=batch_datamodel,
            progress_callback=self.progress_callback,
        )

        ffmpeg_cmd_helper.set_video_settings(
            profile=self.video_profile,
            encoding_speed=self.video_encoding_speed,
            quality=self.video_quality,
        )
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=self.audio_bitrate, video_bitrate=self.video_bitrate)

        ffmpeg_cmd_helper.set_video_filters(
            resolution=self.resolution if self.resolution is not None else None,
        )

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoResizeExternalDependencies",

    "VideoResizeInFormats",
    "VideoResizeOutFormats",

    "VideoResizeProfile",
    "VideoResizeEncoding",
    "VideoResizeQuality",

    "VideoResizeCommand",
]
