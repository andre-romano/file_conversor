
# src\file_conversor\cli\pdf\split_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.cli.pdf._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, SPLIT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption, PasswordOption

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
                name="split",
                description="Split",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{SPLIT_NAME}" "%1""',
                icon=str(icons_folder_path / 'split.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_split_cmd(
    input_files: List[Path],
    password: str | None,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ... ")
        pypdf_backend.split(
            input_file=input_file,
            output_file=output_file,
            password=password,
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p)),
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=True)  # avoid issues with existing files
    cmd_mgr.run(callback)
    logger.info(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf split
@typer_cmd.command(
    name=SPLIT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Split PDF pages into several 1-page PDFs.')}

        {_('For every PDF page, a new single page PDF will be created using the format `input_file_X.pdf`, where X is the page number.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Split pages of input_file.pdf into output_file_X.pdf files')}*:

- `file_conversor {COMMAND_NAME} {SPLIT_NAME} input_file.pdf -od D:/Downloads` 



*{_('For every PDF page, generate a "input_file_X.pdf" file')}*:

- `file_conversor {COMMAND_NAME} {SPLIT_NAME} input_file.pdf` 
""")
def split(
    input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
    password: Annotated[str | None, PasswordOption()] = None,
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_split_cmd(
        input_files=input_files,
        password=password,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_split_cmd",
]
