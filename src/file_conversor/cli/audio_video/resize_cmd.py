
# src\file_conversor\cli\audio_video\resize_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.audio_video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.audio_video._typer import COMMAND_NAME, RESIZE_NAME
from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.formatters import parse_video_resize
from file_conversor.utils.validators import check_positive_integer, check_valid_options
from file_conversor.utils.typer_utils import AxisOption, FormatOption, InputFilesArgument, OutputDirOption

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
    for ext in FFmpegBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="resize",
                description="Resize",
                command=f'cmd /k "{Environment.get_executable()} "{COMMAND_NAME}" "{RESIZE_NAME}" "%1""',
                icon=str(icons_folder_path / "resize.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=RESIZE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Resize a audio/video file.')}

        {_('Outputs a audio/video file with _resized at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {RESIZE_NAME} input_file.webm -rs 1024x768 -od output_dir/ -f mp4 --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {RESIZE_NAME} input_file.mp4 -rs 1280x720`
    """)
def resize(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend)],

    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],

    resolution: Annotated[str | None, typer.Option("--resolution", "-rs",
                                                   help=f'{_("Video target resolution. Format WIDTHxHEIGHT (in pixels). Defaults to None (use same resolution as video source)")}',
                                                   )] = None,

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    # parse width, height
    width, height = parse_video_resize(resolution, prompt=True, quiet=STATE["quiet"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        # display current progress
        process = ffmpeg_backend.convert(
            input_file=input_file,
            output_file=output_file,
            audio_bitrate=audio_bitrate,
            video_bitrate=video_bitrate,
            width=width,
            height=height,
            overwrite_output=STATE["overwrite-output"],
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_resized")

    logger.info(f"{_('FFMpeg resize')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
