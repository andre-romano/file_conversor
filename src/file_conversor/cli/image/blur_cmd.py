
# src\file_conversor\cli\multimedia\blur_cmd.py
import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend
from file_conversor.cli.image._typer import FILTER_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, BLUR_NAME

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


def execute_image_blur_cmd(
    input_files: List[Path],
    radius: int,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.blur(
            input_file=input_file,
            output_file=output_file,
            blur_pixels=radius,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_blurred")

    logger.info(f"{_('Image blur')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=BLUR_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Applies gaussian blur to an image file.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {BLUR_NAME} input_file.jpg -od D:/Downloads`

        - `file_conversor {COMMAND_NAME} {BLUR_NAME} input_file1.bmp -r 3`
    """)
def blur(
    input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
    radius: Annotated[int, RadiusOption()] = 3,
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_blur_cmd(
        input_files=input_files,
        radius=radius,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_blur_cmd",
]
