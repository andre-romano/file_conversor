
# src\file_conversor\cli\xls\convert_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend import LibreofficeCalcBackend

from file_conversor.cli.xls._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Configuration, Environment, Log, State, get_translation

from file_conversor.utils import CommandManager, ProgressManager
from file_conversor.utils.formatters import format_in_out_files_tuple
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = LibreofficeCalcBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # WordBackend commands
    for ext in LibreofficeCalcBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "{ext}""',
                icon=str(icons_folder_path / f"{ext}.ico"),
            )
            for ext in LibreofficeCalcBackend.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_xls_convert_cmd(
    input_files: List[Path],
    format: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
) -> None:
    """Execute the convert command."""

    files = format_in_out_files_tuple(
        input_files=input_files,
        output_dir=output_dir,
        format=format,
    )

    backend = LibreofficeCalcBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )
    with ProgressManager(len(input_files)) as progress_mgr:
        logger.info(f"[bold]{_('Converting files')}[/] ...")
        # Perform conversion
        backend.convert(
            files=files,
            file_processed_callback=lambda _: progress_callback(progress_mgr.complete_step())
        )

    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=CONVERT_NAME,
    help=f"""
        {_('Convert spreadsheet files into other formats (requires LibreOffice).')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.ods -o output_file.xls`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.xlsx -o output_file.pdf`
    """)
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(LibreofficeCalcBackend)],
    format: Annotated[str, FormatOption(LibreofficeCalcBackend)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_xls_convert_cmd(
        input_files=input_files,
        format=format,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_xls_convert_cmd",
]
