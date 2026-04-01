
# src\file_conversor\command\video\enhance_cmd.py

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

VideoEnhanceExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES
VideoEnhanceInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoEnhanceOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoEnhanceAudioCodecs = FFmpegCmdHelper.AudioCodecs
VideoEnhanceVideoCodecs = FFmpegCmdHelper.VideoCodecs

VideoEnhanceProfile = FFmpegCmdHelper.VideoProfile
VideoEnhanceEncoding = FFmpegCmdHelper.VideoEncoding
VideoEnhanceQuality = FFmpegCmdHelper.VideoQuality

VideoEnhanceMirrorAxis = FFmpegCmdHelper.MirrorAxis
VideoEnhanceRotation = FFmpegCmdHelper.Rotation


class VideoEnhanceCommand(AbstractCommand[VideoEnhanceInFormats, VideoEnhanceOutFormats]):
    input_files: list[Path]
    file_format: VideoEnhanceOutFormats
    audio_bitrate: int | None
    video_bitrate: int | None
    video_profile: VideoEnhanceProfile
    video_encoding_speed: VideoEnhanceEncoding
    video_quality: VideoEnhanceQuality
    width: int | None
    height: int | None
    fps: int | None
    brightness: float
    contrast: float
    color: float
    gamma: float
    deshake: bool
    unsharp: bool
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoEnhanceExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoEnhanceInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoEnhanceOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_suffix=self.file_format.value,
            out_stem="_enhanced",
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
            resolution=(self.width, self.height) if self.width is not None and self.height is not None else None,
            fps=self.fps,
            brightness=self.brightness,
            contrast=self.contrast,
            color=self.color,
            gamma=self.gamma,
            deshake=self.deshake,
            unsharp=self.unsharp,
        )

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoEnhanceExternalDependencies",
    "VideoEnhanceInFormats",
    "VideoEnhanceOutFormats",

    "VideoEnhanceAudioCodecs",
    "VideoEnhanceVideoCodecs",

    "VideoEnhanceProfile",
    "VideoEnhanceEncoding",
    "VideoEnhanceQuality",

    "VideoEnhanceMirrorAxis",
    "VideoEnhanceRotation",

    "VideoEnhanceCommand",
]
