
# src\file_conversor\cli\video\mirror_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper, EXTERNAL_DEPENDENCIES

from file_conversor.cli.video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, MIRROR_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_positive_integer
from file_conversor.utils.typer_utils import AudioBitrateOption, AxisOption, FormatOption, InputFilesArgument, OutputDirOption, VideoBitrateOption, VideoEncodingSpeedOption, VideoQualityOption

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
                name="mirror_x",
                description="Mirror X axis",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{MIRROR_NAME}" "%1" -a x"',
                icon=str(icons_folder_path / "left_right.ico"),
            ),
            WinContextCommand(
                name="mirror_y",
                description="Mirror Y axis",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{MIRROR_NAME}" "%1" -a y"',
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
    ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_mirrored", output_dir=output_dir)

    ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
    ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
    ffmpeg_cmd_helper.set_mirror_filter(mirror_axis)

    ffmpeg_cmd_helper.execute()


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
