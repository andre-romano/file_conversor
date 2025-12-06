
# src\file_conversor\cli\video\compress_cmd.py
import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper, EXTERNAL_DEPENDENCIES

from file_conversor.cli.video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, COMPRESS_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption, TargetFileSizeOption, VideoEncodingSpeedOption, VideoQualityOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # IMG2PDF commands
    for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="compress",
                description="Compress",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{COMPRESS_NAME}" "%1""',
                icon=str(icons_folder_path / "compress.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=COMPRESS_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Compress a video file to a target file size.')}

        {_('Outputs an video file with _compressed at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file.avi -od D:/Downloads --target-size 30M`

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file1.mp4 -ts 50M`
    """)
def compress(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

    target_size: Annotated[str, TargetFileSizeOption(prompt=f"{_("Target file size (size[K|M|G]) [0 = do not limit output file size]")}")],

    video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegBackend.ENCODING_SPEEDS)] = CONFIG["video-encoding-speed"],
    video_quality: Annotated[str | None, VideoQualityOption(FFmpegBackend.QUALITY_PRESETS)] = CONFIG["video-quality"],

    file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG["video-format"],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    ffmpeg_cmd_helper = FFmpegCmdHelper(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # Set arguments for FFmpeg command helper
    ffmpeg_cmd_helper.set_input(input_files)
    ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_compressed", output_dir=output_dir)

    ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
    ffmpeg_cmd_helper.set_target_size(target_size)

    ffmpeg_cmd_helper.execute()


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
