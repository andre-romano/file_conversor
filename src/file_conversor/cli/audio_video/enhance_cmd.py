
# src\file_conversor\cli\audio_video\enhance_cmd.py
import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.audio_video._typer import VIDEO_TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.audio_video._typer import COMMAND_NAME, ENHANCE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import AudioBitrateOption, BrightnessOption, ColorOption, ContrastOption, DeshakeOption, FPSOption, FormatOption, GammaOption, InputFilesArgument, OutputDirOption, ResolutionOption, UnsharpOption, VideoBitrateOption
from file_conversor.utils.validators import check_positive_integer

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # IMG2PDF commands
    for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="color",
                description="Color Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --color 1.20',
                icon=str(icons_folder_path / "color.ico"),
            ),
            WinContextCommand(
                name="contrast",
                description="Contrast Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --contrast 1.20',
                icon=str(icons_folder_path / "contrast.ico"),
            ),
            WinContextCommand(
                name="brightness",
                description="Brightness Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --brightness 1.20',
                icon=str(icons_folder_path / "brightness.ico"),
            ),
            WinContextCommand(
                name="gamma",
                description="Gamma Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --gamma 1.20',
                icon=str(icons_folder_path / "gamma.ico"),
            ),
            WinContextCommand(
                name="to_30fps",
                description="To 30 FPS",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --fps 30',
                icon=str(icons_folder_path / "30.ico"),
            ),
            WinContextCommand(
                name="to_60fps",
                description="To 60 FPS",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --fps 60',
                icon=str(icons_folder_path / "60.ico"),
            ),
            WinContextCommand(
                name="sharpness",
                description="Sharpness Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --unsharp',
                icon=str(icons_folder_path / "sharpener.ico"),
            ),
            WinContextCommand(
                name="deshake",
                description="Deshake",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --deshake',
                icon=str(icons_folder_path / "shaking.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=ENHANCE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Enhance video bitrate, resolution, fps, color, brightness, etc.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file.avi -od D:/Downloads --color 1.20`

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file1.mp4 --unsharp`

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file.mkv -cl 0.85 -b 1.10`        
    """)
def enhance(
    input_files: Annotated[List[str], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

    file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG["video-format"],

    audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG["audio-bitrate"],
    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    resolution: Annotated[str | None, ResolutionOption()] = None,
    fps: Annotated[int | None, FPSOption()] = None,

    color: Annotated[float, ColorOption()] = 1.0,
    brightness: Annotated[float, BrightnessOption()] = 1.0,
    contrast: Annotated[float, ContrastOption()] = 1.0,
    gamma: Annotated[float, GammaOption()] = 1.0,

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
        # eq
        brightness=brightness,
        contrast=contrast,
        color=color,
        gamma=gamma,
        # image
        resolution=resolution,
        fps=fps,
        deshake=deshake,
        unsharp=unsharp,
    )

    two_pass = (video_bitrate > 0) or (audio_bitrate > 0)

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(bitrate=audio_bitrate, filters=audio_filters)
        ffmpeg_backend.set_video_codec(bitrate=video_bitrate, filters=video_filters)

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
    cmd_mgr.run(callback, out_stem="_enhanced", out_suffix=f".{file_format}")

    logger.info(f"{_('FFMpeg enhance')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
