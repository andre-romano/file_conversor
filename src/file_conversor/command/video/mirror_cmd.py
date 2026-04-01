
# src\file_conversor\command\video\mirror_cmd.py

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


VideoMirrorExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

VideoMirrorInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoMirrorOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoMirrorProfile = FFmpegCmdHelper.VideoProfile
VideoMirrorEncoding = FFmpegCmdHelper.VideoEncoding
VideoMirrorQuality = FFmpegCmdHelper.VideoQuality

VideoMirrorAxis = FFmpegCmdHelper.MirrorAxis


class VideoMirrorCommand(AbstractCommand[VideoMirrorInFormats, VideoMirrorOutFormats]):
    input_files: list[Path]
    mirror_axis: VideoMirrorAxis | None
    file_format: VideoMirrorOutFormats
    audio_bitrate: int | None
    video_bitrate: int | None
    video_profile: VideoMirrorProfile
    video_encoding_speed: VideoMirrorEncoding
    video_quality: VideoMirrorQuality
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoMirrorExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoMirrorInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoMirrorOutFormats

    @override
    def execute(self):
        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            out_stem="_mirrored",
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
            mirror_axis=self.mirror_axis,
        )

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoMirrorExternalDependencies",

    "VideoMirrorInFormats",
    "VideoMirrorOutFormats",

    "VideoMirrorProfile",
    "VideoMirrorEncoding",
    "VideoMirrorQuality",

    "VideoMirrorAxis",

    "VideoMirrorCommand",
]
