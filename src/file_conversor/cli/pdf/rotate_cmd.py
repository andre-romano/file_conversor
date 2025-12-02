
# src\file_conversor\cli\pdf\rotate_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.cli.pdf._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, ROTATE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption, PasswordOption
from file_conversor.utils.formatters import parse_pdf_rotation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in PyPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="rotate_anticlock_90",
                description="Rotate Left",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r "1-:-90""',
                icon=str(icons_folder_path / "rotate_left.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_90",
                description="Rotate Right",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r "1-:90""',
                icon=str(icons_folder_path / "rotate_right.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_rotate_cmd(
    input_files: List[Path],
    rotation: List[str],
    password: str | None,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.rotate(
            input_file=input_file,
            output_file=output_file,
            decrypt_password=password,
            rotations=parse_pdf_rotation(rotation, pypdf_backend.len(input_file)),
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p)),
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_rotated")
    logger.info(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/].")


@typer_cmd.command(
    name=ROTATE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Rotate PDF pages (clockwise or anti-clockwise).')}
        
        {_('Outputs a file with _rotated at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Rotate page 1 by 180 degress')}*:

- `file_conversor {COMMAND_NAME} {ROTATE_NAME} input_file.pdf -o output_file.pdf -r "1:180"` 



*{_('Rotate page 5-7 by 90 degress, 9 by -90 degrees, 10-15 by 180 degrees')}*:

- `file_conversor {COMMAND_NAME} {ROTATE_NAME} input_file.pdf -r "5-7:90" -r "9:-90" -r "10-15:180"`
    """)
def rotate(
    input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
    rotation: Annotated[List[str], typer.Option("--rotation", "-r",
                                                help=_("List of pages to rotate. Format ``\"page:rotation\"`` or ``\"start-end:rotation\"`` or ``\"start-:rotation\"`` ..."),
                                                )],
    password: Annotated[str | None, PasswordOption()] = None,
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_rotate_cmd(
        input_files=input_files,
        rotation=rotation,
        password=password,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_rotate_cmd",
]
