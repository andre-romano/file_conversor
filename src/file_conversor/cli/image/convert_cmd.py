
# src\file_conversor\cli\image\convert_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List
from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.cli.image._typer import CONVERSION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption, QualityOption

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
    # Pillow commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "jpg" -q 90"',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "png" -q 90"',
                icon=str(icons_folder_path / 'png.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_convert_cmd(
    input_files: List[Path],
    format: str,
    quality: int,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda progress: None,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.convert(
            input_file=input_file,
            output_file=output_file,
            quality=quality,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('Image convertion')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=CONVERT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a image file to a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.webp -f jpg --quality 85`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.bmp -f png -od D:/Downloads`
    """)
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
    format: Annotated[str, FormatOption(PillowBackend)],
    quality: Annotated[int, QualityOption()] = CONFIG["image-quality"],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_convert_cmd(
        input_files=input_files,
        format=format,
        quality=quality,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_convert_cmd",
]
