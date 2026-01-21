
# src\file_conversor\cli\video\convert_cmd.py

from typing import Annotated, Any, Callable, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import (InputFilesArgument, FormatOption, OutputDirOption,
                                             AudioBitrateOption, VideoBitrateOption,
                                             AudioCodecOption, VideoCodecOption,
                                             AxisOption,
                                             BrightnessOption, ColorOption, ContrastOption, GammaOption,
                                             VideoRotationOption, DeshakeOption, UnsharpOption,
                                             FPSOption, ResolutionOption,
                                             VideoEncodingSpeedOption, VideoQualityOption)

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoConvertTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_mkv",
                    description="To MKV",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f mkv "%1""',
                    icon=str(icons_folder_path / 'mkv.ico'),
                ),
                WinContextCommand(
                    name="to_mp4",
                    description="To MP4",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f mp4 "%1""',
                    icon=str(icons_folder_path / 'mp4.ico'),
                ),
                WinContextCommand(
                    name="to_webm",
                    description="To WEBM",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f webm "%1""',
                    icon=str(icons_folder_path / 'webm.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert a video file to another video format.'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -f mkv -od output_dir/ --audio-bitrate 192`

    - `file_conversor {group_name} {command_name} input_file.mp4 -f avi -r 90`

    - `file_conversor {group_name} {command_name} input_file.avi -f mp4 -rs 1280:720`
""")

    def convert(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS)],

        file_format: Annotated[str, FormatOption(FFmpegCmdHelper.BACKEND.SUPPORTED_OUT_VIDEO_FORMATS)],

        audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG.video_bitrate,

        audio_codec: Annotated[str | None, AudioCodecOption(FFmpegCmdHelper.BACKEND.get_supported_audio_codecs())] = None,
        video_codec: Annotated[str | None, VideoCodecOption(FFmpegCmdHelper.BACKEND.get_supported_video_codecs())] = None,

        video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegCmdHelper.BACKEND.ENCODING_SPEEDS)] = CONFIG.video_encoding_speed,
        video_quality: Annotated[str | None, VideoQualityOption(FFmpegCmdHelper.BACKEND.QUALITY_PRESETS)] = CONFIG.video_quality,

        resolution: Annotated[str | None, ResolutionOption()] = None,
        fps: Annotated[int | None, FPSOption()] = None,

        brightness: Annotated[float, BrightnessOption()] = 1.0,
        contrast: Annotated[float, ContrastOption()] = 1.0,
        color: Annotated[float, ColorOption()] = 1.0,
        gamma: Annotated[float, GammaOption()] = 1.0,

        rotation: Annotated[int | None, VideoRotationOption()] = None,
        mirror_axis: Annotated[str | None, AxisOption()] = None,
        deshake: Annotated[bool, DeshakeOption()] = False,
        unsharp: Annotated[bool, UnsharpOption()] = False,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        # Set arguments for FFmpeg command helper
        ffmpeg_cmd_helper.set_input(input_files)
        ffmpeg_cmd_helper.set_output(file_format=file_format, output_dir=output_dir)

        ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
        ffmpeg_cmd_helper.set_codecs(audio_codec=audio_codec, video_codec=video_codec)

        ffmpeg_cmd_helper.set_resolution_filter(resolution)
        ffmpeg_cmd_helper.set_fps_filter(fps)
        ffmpeg_cmd_helper.set_enhancement_filters(
            brightness=brightness,
            contrast=contrast,
            color=color,
            gamma=gamma,
        )
        ffmpeg_cmd_helper.set_rotation_filter(rotation)
        ffmpeg_cmd_helper.set_mirror_filter(mirror_axis)
        ffmpeg_cmd_helper.set_deshake_filter(deshake)
        ffmpeg_cmd_helper.set_unsharp_filter(unsharp)

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoConvertTyperCommand",
]
