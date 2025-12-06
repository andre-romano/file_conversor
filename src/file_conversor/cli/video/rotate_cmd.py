
# src\file_conversor\cli\video\rotate_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper, EXTERNAL_DEPENDENCIES

from file_conversor.cli.video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, ROTATE_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_positive_integer, check_valid_options
from file_conversor.utils.typer_utils import AudioBitrateOption, FormatOption, InputFilesArgument, OutputDirOption, VideoBitrateOption, VideoEncodingSpeedOption, VideoQualityOption, VideoRotationOption

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
                name="rotate_anticlock_90",
                description="Rotate Left",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r -90"',
                icon=str(icons_folder_path / "rotate_left.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_90",
                description="Rotate Right",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r 90"',
                icon=str(icons_folder_path / "rotate_right.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=ROTATE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Rotate a video file (clockwise or anti-clockwise).')}

        {_('Outputs an video file with _rotated at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {ROTATE_NAME} input_file.webm -r 90 -od output_dir/ --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {ROTATE_NAME} input_file.mp4 -r 180`
    """)
def rotate(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

    rotation: Annotated[int, VideoRotationOption()],

    file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG["video-format"],

    audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG["audio-bitrate"],
    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegBackend.ENCODING_SPEEDS)] = CONFIG["video-encoding-speed"],
    video_quality: Annotated[str | None, VideoQualityOption(FFmpegBackend.QUALITY_PRESETS)] = CONFIG["video-quality"],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):

    ffmpeg_cmd_helper = FFmpegCmdHelper(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # Set arguments for FFmpeg command helper
    ffmpeg_cmd_helper.set_input(input_files)
    ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_rotated", output_dir=output_dir)

    ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
    ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
    ffmpeg_cmd_helper.set_rotation_filter(rotation)

    ffmpeg_cmd_helper.execute()


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
