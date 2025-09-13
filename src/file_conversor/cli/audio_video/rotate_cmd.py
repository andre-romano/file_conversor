
# src\file_conversor\cli\audio_video\rotate_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.audio_video._typer import VIDEO_TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.audio_video._typer import COMMAND_NAME, ROTATE_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_positive_integer, check_valid_options
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption, VideoBitrateOption, VideoRotationOption

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
                name="rotate_anticlock_90",
                description="Rotate Left",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r -90',
                icon=str(icons_folder_path / "rotate_left.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_90",
                description="Rotate Right",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r 90',
                icon=str(icons_folder_path / "rotate_right.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_180",
                description="Rotate 180",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r 180',
                icon=str(icons_folder_path / "180_degrees.ico"),
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

    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    video_filters = ffmpeg_backend.build_video_filters(
        rotation=rotation,
    )

    two_pass = video_bitrate > 0

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(codec="copy")
        ffmpeg_backend.set_video_codec(bitrate=video_bitrate, filters=video_filters)

        process = ffmpeg_backend.execute(
            progress_callback=progress_mgr.update_progress,
            pass_num=1 if two_pass else 0,
        )
        progress_mgr.complete_step()

        if two_pass:
            # display current progress
            process = ffmpeg_backend.execute(
                progress_callback=progress_mgr.update_progress,
                pass_num=2,
            )
            progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, steps=2 if two_pass else 1, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_rotated", out_suffix=f".{file_format}")

    logger.info(f"{_('FFMpeg rotate')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
