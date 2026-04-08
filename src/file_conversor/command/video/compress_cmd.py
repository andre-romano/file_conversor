
# src\file_conversor\command\video\compress_cmd.py

from pathlib import Path
from typing import override

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel
from file_conversor.command.video._ffmpeg_cmd_helper import FFmpegCmdHelper
from file_conversor.config import CONFIG, LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

VideoCompressExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

VideoCompressInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoCompressOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoCompressProfile = FFmpegCmdHelper.VideoProfile
VideoCompressEncoding = FFmpegCmdHelper.VideoEncoding
VideoCompressQuality = FFmpegCmdHelper.VideoQuality


class VideoCompressCommand(AbstractCommand[VideoCompressInFormats, VideoCompressOutFormats]):
    input_files: list[Path]
    file_format: VideoCompressOutFormats
    target_size: str
    video_profile: VideoCompressProfile
    video_encoding_speed: VideoCompressEncoding
    video_quality: VideoCompressQuality
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoCompressExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoCompressInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoCompressOutFormats

    @override
    def execute(self):

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem="_compressed",
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
        ffmpeg_cmd_helper.set_target_size(self.target_size)

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoCompressExternalDependencies",
    "VideoCompressInFormats",
    "VideoCompressOutFormats",
    "VideoCompressProfile",
    "VideoCompressEncoding",
    "VideoCompressQuality",
    "VideoCompressCommand",
]
