
# src\file_conversor\cli\image\render_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List
from rich import print

# user-provided modules
from file_conversor.backend.image import PyMuSVGBackend

from file_conversor.cli.image._typer import CONVERSION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, RENDER_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import DPIOption, FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PyMuSVGBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # PyMuSVGBackend commands
    for ext in PyMuSVGBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{RENDER_NAME}" "%1" -f "jpg""',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{RENDER_NAME}" "%1" -f "png""',
                icon=str(icons_folder_path / 'png.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_render_cmd(
    input_files: List[Path],
    format: str,
    dpi: int,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pymusvg_backend = PyMuSVGBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pymusvg_backend.convert(
            input_file=input_file,
            output_file=output_file,
            dpi=dpi,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('Image render')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=RENDER_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Render an image vector file into a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {RENDER_NAME} input_file.svg -f png`

        - `file_conversor {COMMAND_NAME} {RENDER_NAME} input_file.svg input_file2.svg -od D:/Downloads -f jpg --dpi 300`
    """)
def render(
    input_files: Annotated[List[Path], InputFilesArgument(PyMuSVGBackend)],
    format: Annotated[str, FormatOption(PyMuSVGBackend)],
    dpi: Annotated[int, DPIOption()] = CONFIG["image-dpi"],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_render_cmd(
        input_files=input_files,
        format=format,
        dpi=dpi,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_render_cmd",
]
