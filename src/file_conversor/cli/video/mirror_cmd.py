
# src\file_conversor\cli\video\mirror_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._ffmpeg_cmd import _ffmpeg_cli_cmd

from file_conversor.cli.video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, MIRROR_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_positive_integer
from file_conversor.utils.typer_utils import AxisOption, FormatOption, InputFilesArgument, OutputDirOption, VideoBitrateOption, VideoEncodingSpeedOption, VideoQualityOption

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="mirror_x",
                description="Mirror X axis",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{MIRROR_NAME}" "%1" -a x',
                icon=str(icons_folder_path / "left_right.ico"),
            ),
            WinContextCommand(
                name="mirror_y",
                description="Mirror Y axis",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{MIRROR_NAME}" "%1" -a y',
                icon=str(icons_folder_path / "up_down.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=MIRROR_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Mirror a video file (vertically or horizontally).')}

        {_('Outputs a video file with _mirrored at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {MIRROR_NAME} input_file.webm -a x -od output_dir/ --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {MIRROR_NAME} input_file.mp4 -a y`
    """)
def mirror(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

    mirror_axis: Annotated[str, AxisOption()],

    file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG["video-format"],

    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption()] = CONFIG["video-encoding-speed"],
    video_quality: Annotated[str | None, VideoQualityOption()] = CONFIG["video-quality"],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    _ffmpeg_cli_cmd(
        input_files,
        file_format=file_format,
        out_stem="_mirrored",
        mirror_axis=mirror_axis,
        video_bitrate=video_bitrate,
        video_encoding_speed=video_encoding_speed,
        video_quality=video_quality,
        output_dir=output_dir,
    )
