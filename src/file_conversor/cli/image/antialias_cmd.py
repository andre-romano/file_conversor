
# src\file_conversor\cli\multimedia\antialias_cmd.py
import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend
from file_conversor.cli.image._typer import FILTER_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, ANTIALIAS_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption, RadiusOption
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
                name="antialias",
                description="Antialias",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{ANTIALIAS_NAME}" "%1" -r 3',
                icon=str(icons_folder_path / "diagonal_line.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=ANTIALIAS_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Applies antialias filter to an image file.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {ANTIALIAS_NAME} input_file1.bmp -r 5`

        - `file_conversor {COMMAND_NAME} {ANTIALIAS_NAME} input_file.jpg -r 2 -a mode`        
    """)
def antialias(
    input_files: Annotated[List[str], InputFilesArgument(PillowBackend)],

    radius: Annotated[int, RadiusOption()] = 3,

    algorithm: Annotated[str, typer.Option("--algorithm", "-a",
                                           help=f'{_("Algorithm to use. Available algorihtms:")} median, mode.',
                                           callback=lambda x: check_valid_options(x, ["median", "mode"]),
                                           )] = "median",

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.antialias(
            input_file=input_file,
            output_file=output_file,
            radius=radius,
            algorithm=algorithm,
        )
        progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_antialiased")

    logger.info(f"{_('Image antialiasing')}: [green bold]{_('SUCCESS')}[/]")
