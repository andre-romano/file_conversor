
# src\file_conversor\command\video\convert_cmd.py

from pathlib import Path
from typing import override

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel
from file_conversor.command.video._ffmpeg_cmd_helper import FFmpegCmdHelper
from file_conversor.config import CONFIG, LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


VideoConvertExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES
VideoConvertInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoConvertOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoConvertAudioCodecs = FFmpegCmdHelper.AudioCodecs
VideoConvertVideoCodecs = FFmpegCmdHelper.VideoCodecs

VideoConvertProfile = FFmpegCmdHelper.VideoProfile
VideoConvertEncoding = FFmpegCmdHelper.VideoEncoding
VideoConvertQuality = FFmpegCmdHelper.VideoQuality

VideoConvertMirrorAxis = FFmpegCmdHelper.MirrorAxis
VideoConvertRotation = FFmpegCmdHelper.Rotation


class VideoConvertCommand(AbstractCommand[VideoConvertInFormats, VideoConvertOutFormats]):
    input_files: list[Path]
    file_format: VideoConvertOutFormats
    audio_bitrate: int | None
    video_bitrate: int | None
    audio_codec: VideoConvertAudioCodecs | None
    video_codec: VideoConvertVideoCodecs | None
    video_profile: VideoConvertProfile
    video_encoding_speed: VideoConvertEncoding
    video_quality: VideoConvertQuality
    width: int | None
    height: int | None
    fps: int | None
    brightness: float
    contrast: float
    color: float
    gamma: float
    rotation: VideoConvertRotation | None
    mirror_axis: VideoConvertMirrorAxis | None
    deshake: bool
    unsharp: bool
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoConvertExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoConvertInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoConvertOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
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
        ffmpeg_cmd_helper.set_codecs(audio_codec=self.audio_codec, video_codec=self.video_codec)

        ffmpeg_cmd_helper.set_video_filters(
            resolution=(self.width, self.height) if self.width is not None and self.height is not None else None,
            fps=self.fps,
            brightness=self.brightness,
            contrast=self.contrast,
            color=self.color,
            gamma=self.gamma,
            rotation=self.rotation,
            mirror_axis=self.mirror_axis,
            deshake=self.deshake,
            unsharp=self.unsharp,
        )

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoConvertExternalDependencies",
    "VideoConvertInFormats",
    "VideoConvertOutFormats",

    "VideoConvertAudioCodecs",
    "VideoConvertVideoCodecs",

    "VideoConvertProfile",
    "VideoConvertEncoding",
    "VideoConvertQuality",

    "VideoConvertMirrorAxis",
    "VideoConvertRotation",

    "VideoConvertCommand",
]
