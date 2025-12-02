
# src\file_conversor\cli\pdf\merge_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.cli.pdf._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, MERGE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputFileOption, PasswordOption
from file_conversor.utils.validators import check_path_exists

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES


def execute_pdf_merge_cmd(
    input_files: List[Path],
    password: str | None,
    output_file: Path | None,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    output_file = output_file if output_file else Path() / CommandManager.get_output_file(input_files[0], stem="_merged")
    if not STATE["overwrite-output"]:
        check_path_exists(output_file, exists=False)

    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with ProgressManager() as progress_mgr:
        print(f"Processing '{output_file}' ...")
        pypdf_backend.merge(
            # files
            input_files=input_files,
            output_file=output_file,
            password=password,
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
        )
        progress_callback(progress_mgr.complete_step())

    logger.info(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/].")


@typer_cmd.command(
    name=MERGE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Merge (join) input PDFs into a single PDF file.')}
        
        {_('Outputs a file with _merged at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Merge files "input_file1.pdf" and "input_file2.pdf" into "output_file.pdf"')}*:

- `file_conversor {COMMAND_NAME} {MERGE_NAME} "input_file1.pdf" "input_file2.pdf" -of output_file.pdf` 



*{_('Merge protected PDFs "input_file1.pdf" and "input_file2.pdf" with password "unlock_password"')}*:

- `file_conversor {COMMAND_NAME} {MERGE_NAME} "input_file1.pdf" "input_file2.pdf" -p "unlock_password" -of output_file.pdf` 
    """)
def merge(
    input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
    password: Annotated[str | None, PasswordOption()] = None,
    output_file: Annotated[Path | None, OutputFileOption(PyPDFBackend)] = None,
):
    execute_pdf_merge_cmd(
        input_files=input_files,
        password=password,
        output_file=output_file,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_merge_cmd",
]
