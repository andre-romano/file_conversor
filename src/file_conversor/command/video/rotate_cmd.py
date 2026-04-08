
# src\file_conversor\command\video\rotate_cmd.py

from pathlib import Path
from typing import override

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel
from file_conversor.command.video._ffmpeg_cmd_helper import FFmpegCmdHelper
from file_conversor.config import CONFIG, LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


VideoRotateExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

VideoRotateInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoRotateOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoRotateProfile = FFmpegCmdHelper.VideoProfile
VideoRotateEncoding = FFmpegCmdHelper.VideoEncoding
VideoRotateQuality = FFmpegCmdHelper.VideoQuality

VideoRotateRotation = FFmpegCmdHelper.Rotation


class VideoRotateCommand(AbstractCommand[VideoRotateInFormats, VideoRotateOutFormats]):
    input_files: list[Path]
    rotation: VideoRotateRotation | None
    file_format: VideoRotateOutFormats
    audio_bitrate: int | None
    video_bitrate: int | None
    video_profile: VideoRotateProfile
    video_encoding_speed: VideoRotateEncoding
    video_quality: VideoRotateQuality
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoRotateExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoRotateInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoRotateOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem="_rotated",
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
            rotation=self.rotation,
        )

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoRotateExternalDependencies",

    "VideoRotateInFormats",
    "VideoRotateOutFormats",

    "VideoRotateProfile",
    "VideoRotateEncoding",
    "VideoRotateQuality",

    "VideoRotateRotation",
    "VideoRotateCommand",
]
