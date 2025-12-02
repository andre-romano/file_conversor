
# src\file_conversor\cli\pdf\extract_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.cli.pdf._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, EXTRACT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption, PasswordOption
from file_conversor.utils.formatters import parse_pdf_pages

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
                name="extract",
                description="Extract",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{EXTRACT_NAME}" "%1""',
                icon=str(icons_folder_path / 'extract.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_extract_cmd(
    input_files: List[Path],
    pages: List[str] | str | None,
    password: str | None,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.extract(
            input_file=input_file,
            output_file=output_file,
            password=password,
            pages=parse_pdf_pages(pages),
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_extracted")

    logger.info(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/].")


@typer_cmd.command(
    name=EXTRACT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Extract specific pages from a PDF.')}
        
        {_('Outputs a file with _extracted at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Extract pages 1 to 2, 4 and 6')}*:

- `file_conversor {COMMAND_NAME} {EXTRACT_NAME} input_file.pdf -pg 1-2 -pg 4-4 -pg 6-6 -od D:/Downloads` 
    """)
def extract(
    input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
    pages: Annotated[List[str] | None, typer.Option("--pages", "-pg",
                                                    help=_('Pages to extract (comma-separated list). Format "start-end".'),
                                                    )] = None,
    password: Annotated[str | None, PasswordOption()] = None,
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_extract_cmd(
        input_files=input_files,
        pages=pages,
        password=password,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_extract_cmd",
]
