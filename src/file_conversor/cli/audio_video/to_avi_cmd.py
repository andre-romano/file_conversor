
# src\file_conversor\cli\audio_video\to_avi_cmd.py

import sys
import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter

from file_conversor.cli.audio_video._typer import CONVERSION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.audio_video._typer import COMMAND_NAME, TO_AVI_NAME
from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import AudioBitrateOption, AudioCodecOption, AxisOption, BrightnessOption, ColorOption, ContrastOption, DeshakeOption, FPSOption, GammaOption, InputFilesArgument, OutputDirOption, ResolutionOption, UnsharpOption, VideoBitrateOption, VideoCodecOption, VideoRotationOption

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

OUTPUT_FILE_FORMAT = "avi"


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_avi",
                description="To AVI",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{TO_AVI_NAME}" "%1"',
                icon=str(icons_folder_path / 'avi.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=TO_AVI_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a video file to')} .{OUTPUT_FILE_FORMAT.upper()} {('format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {TO_AVI_NAME} input_file.webm -od output_dir/ --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {TO_AVI_NAME} input_file.mp4 -r 90`

        - `file_conversor {COMMAND_NAME} {TO_AVI_NAME} input_file.mkv -rs 1280:720`
    """)
def to_avi(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

    audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG["audio-bitrate"],
    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    audio_codec: Annotated[str | None, AudioCodecOption(FFmpegBackend.get_supported_audio_codecs(OUTPUT_FILE_FORMAT))] = None,
    video_codec: Annotated[str | None, VideoCodecOption(FFmpegBackend.get_supported_video_codecs(OUTPUT_FILE_FORMAT))] = None,

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
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # set filters
    audio_filters = ffmpeg_backend.build_audio_filters()
    video_filters = ffmpeg_backend.build_video_filters(
        # image quality
        resolution=resolution,
        fps=fps,

        # EQ
        brightness=brightness,
        contrast=contrast,
        color=color,
        gamma=gamma,

        # transform
        rotation=rotation,
        mirror_axis=mirror_axis,
        deshake=deshake,
        unsharp=unsharp,
    )

    two_pass = (video_bitrate > 0) or (audio_bitrate > 0)

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(codec=audio_codec, bitrate=audio_bitrate, filters=audio_filters)
        ffmpeg_backend.set_video_codec(codec=video_codec, bitrate=video_bitrate, filters=video_filters)

        # display current progress
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
    cmd_mgr.run(callback, out_suffix=f".{OUTPUT_FILE_FORMAT}")

    logger.info(f"{_('FFMpeg convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
