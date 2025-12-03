
# src\file_conversor\cli\multimedia\enhance_cmd.py
import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend
from file_conversor.cli.image._typer import FILTER_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, ENHANCE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import BrightnessOption, ColorOption, ContrastOption, InputFilesArgument, OutputDirOption, SharpnessOption
from file_conversor.utils.validators import is_close

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # IMG2PDF commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="enhance",
                description="Enhance",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1""',
                icon=str(icons_folder_path / "color.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_enhance_cmd(
    input_files: List[Path],
    brightness: float,
    contrast: float,
    color: float,
    sharpness: float,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.enhance(
            input_file=input_file,
            output_file=output_file,
            color_factor=color,
            brightness_factor=brightness,
            contrast_factor=contrast,
            sharpness_factor=sharpness,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_enhanced")

    logger.info(f"{_('Image enhance')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=ENHANCE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Enhance image color, brightness, contrast, or sharpness.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file.jpg -od D:/Downloads --color 1.20`

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file1.bmp --sharpness 0.85`

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file.jpg -cl 0.85 -b 1.10`        
    """)
def enhance(
    input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],

    brightness: Annotated[float, BrightnessOption()] = 1.00,

    contrast: Annotated[float, ContrastOption()] = 1.00,

    color: Annotated[float, ColorOption()] = 1.00,

    sharpness: Annotated[float, SharpnessOption()] = 1.00,

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    if is_close(brightness, 1.00) and is_close(contrast, 1.00) and is_close(color, 1.00) and is_close(sharpness, 1.00):
        brightness = typer.prompt("Brightness factor (> 1.0 increases, < 1.0 decreases)", default=1.00)
        contrast = typer.prompt("Contrast factor (> 1.0 increases, < 1.0 decreases)", default=1.00)
        color = typer.prompt("Color factor (> 1.0 increases, < 1.0 decreases)", default=1.00)
        sharpness = typer.prompt("Sharpness factor (> 1.0 increases, < 1.0 decreases)", default=1.00)

    execute_image_enhance_cmd(
        input_files=input_files,
        brightness=brightness,
        contrast=contrast,
        color=color,
        sharpness=sharpness,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_enhance_cmd",
]
