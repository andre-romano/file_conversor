
# src\file_conversor\cli\video\convert_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper, EXTERNAL_DEPENDENCIES

from file_conversor.cli.video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import (InputFilesArgument, FormatOption, OutputDirOption,
                                              AudioBitrateOption, VideoBitrateOption,
                                              AudioCodecOption, VideoCodecOption,
                                              AxisOption,
                                              BrightnessOption, ColorOption, ContrastOption, GammaOption,
                                              VideoRotationOption, DeshakeOption, UnsharpOption,
                                              FPSOption, ResolutionOption,
                                              VideoEncodingSpeedOption, VideoQualityOption)

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_mkv",
                description="To MKV",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" -f mkv "%1""',
                icon=str(icons_folder_path / 'mkv.ico'),
            ),
            WinContextCommand(
                name="to_mp4",
                description="To MP4",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" -f mp4 "%1""',
                icon=str(icons_folder_path / 'mp4.ico'),
            ),
            WinContextCommand(
                name="to_webm",
                description="To WEBM",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" -f webm "%1""',
                icon=str(icons_folder_path / 'webm.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CONVERT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a video file to another video format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.webm -f mkv -od output_dir/ --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.mp4 -f avi -r 90`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.avi -f mp4 -rs 1280:720`
    """)
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

    file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)],

    audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG["audio-bitrate"],
    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    audio_codec: Annotated[str | None, AudioCodecOption(FFmpegBackend.get_supported_audio_codecs())] = None,
    video_codec: Annotated[str | None, VideoCodecOption(FFmpegBackend.get_supported_video_codecs())] = None,

    video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegBackend.ENCODING_SPEEDS)] = CONFIG["video-encoding-speed"],
    video_quality: Annotated[str | None, VideoQualityOption(FFmpegBackend.QUALITY_PRESETS)] = CONFIG["video-quality"],

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
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
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
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
