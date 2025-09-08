
# src\file_conversor\cli\multimedia\enhance_cmd.py
import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend
from file_conversor.cli.image._typer import FILTER_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, ENHANCE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption
from file_conversor.utils.validators import check_is_bool_or_none, check_path_exists, check_valid_options

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
                name="color",
                description="Color Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --color 1.20',
                icon=str(icons_folder_path / "color.ico"),
            ),
            WinContextCommand(
                name="contrast",
                description="Contrast Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --constrast 1.20',
                icon=str(icons_folder_path / "contrast.ico"),
            ),
            WinContextCommand(
                name="brightness",
                description="Brightness Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --brightness 1.20',
                icon=str(icons_folder_path / "brightness.ico"),
            ),
            WinContextCommand(
                name="sharpness",
                description="Sharpness Up",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ENHANCE_NAME}" "%1" --sharpness 1.20',
                icon=str(icons_folder_path / "sharpener.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=ENHANCE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Enhance image file color, brightness, contrast, or sharpness.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file.jpg -od D:/Downloads --color 1.20`

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file1.bmp --sharpness 0.85`

        - `file_conversor {COMMAND_NAME} {ENHANCE_NAME} input_file.jpg -cl 0.85 -b 1.10`        
    """)
def enhance(
    input_files: Annotated[List[str], InputFilesArgument(PillowBackend)],

    brightness: Annotated[float, typer.Option("--brightness", "-b",
                                              help=_("Adjust image brightness. brightness = 1.00 means no change. brightness < 1.00 makes image black. brightness > 1.00 makes image lighter."),
                                              )] = 1.00,

    contrast: Annotated[float, typer.Option("--contrast", "-ct",
                                            help=_("Adjust image contrast. contrast = 1.00 means no change. contrast < 1.00 reduces contrast (grayish image). contrast > 1.00 increases contrast."),
                                            )] = 1.00,

    color: Annotated[float, typer.Option("--color", "-cl",
                                         help=_("Adjust image color. color = 1.00 means no change. color < 1.00 reduces color saturation. color > 1.00 increases color saturation."),
                                         )] = 1.00,

    sharpness: Annotated[float, typer.Option("--sharpness", "-s",
                                             help=_("Adjust image sharpness. sharpness = 1.00 means no change. sharpness < 1.00 makes image more blurry. sharpness > 1.00 increases image crispness (and noise as well)."),
                                             )] = 1.00,

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
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
        progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_enhanced")

    logger.info(f"{_('Image enhance')}: [green bold]{_('SUCCESS')}[/]")
