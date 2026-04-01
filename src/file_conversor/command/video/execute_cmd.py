
# src\file_conversor\command\video\execute_cmd.py

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

VideoExecuteExternalDependencies = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES
VideoExecuteInFormats = FFmpegCmdHelper.BACKEND.SupportedInVideoFormats
VideoExecuteOutFormats = FFmpegCmdHelper.BACKEND.SupportedOutVideoFormats

VideoExecuteAudioCodecs = FFmpegCmdHelper.AudioCodecs
VideoExecuteVideoCodecs = FFmpegCmdHelper.VideoCodecs

VideoExecuteProfile = FFmpegCmdHelper.VideoProfile
VideoExecuteEncoding = FFmpegCmdHelper.VideoEncoding
VideoExecuteQuality = FFmpegCmdHelper.VideoQuality

VideoExecuteMirrorAxis = FFmpegCmdHelper.MirrorAxis
VideoExecuteRotation = FFmpegCmdHelper.Rotation


class VideoExecuteCommand(AbstractCommand[VideoExecuteInFormats, VideoExecuteOutFormats]):
    input_files: list[Path]
    file_format: VideoExecuteOutFormats
    audio_bitrate: int | None
    video_bitrate: int | None
    audio_codec: VideoExecuteAudioCodecs | None
    video_codec: VideoExecuteVideoCodecs | None
    audio_filters: list[str]
    video_filters: list[str]
    ffmpeg_args: str
    output_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoExecuteExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoExecuteInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoExecuteOutFormats

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

        # set filters
        ffmpeg_cmd_helper.set_audio_filters(custom_filters=self.audio_filters)
        ffmpeg_cmd_helper.set_video_filters(custom_filters=self.video_filters)

        ffmpeg_cmd_helper.set_codecs(audio_codec=self.audio_codec, video_codec=self.video_codec)
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=self.audio_bitrate, video_bitrate=self.video_bitrate)

        ffmpeg_cmd_helper.set_ffmpeg_args(self.ffmpeg_args)

        ffmpeg_cmd_helper.execute()

        logger.info(f"{_('FFMpeg execution')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "VideoExecuteExternalDependencies",
    "VideoExecuteInFormats",
    "VideoExecuteOutFormats",

    "VideoExecuteAudioCodecs",
    "VideoExecuteVideoCodecs",

    "VideoExecuteProfile",
    "VideoExecuteEncoding",
    "VideoExecuteQuality",

    "VideoExecuteMirrorAxis",
    "VideoExecuteRotation",

    "VideoExecuteCommand",
]
