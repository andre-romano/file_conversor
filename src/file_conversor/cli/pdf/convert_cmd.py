
# src\file_conversor\cli\pdf\convert_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyMuPDFBackend, PDF2DOCXBackend

from file_conversor.cli.pdf._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.cli.doc.convert_cmd import execute_doc_convert_cmd

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.formatters import format_in_out_files_tuple
from file_conversor.utils.typer_utils import DPIOption, FormatOption, InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES: set[str] = {
    *PyMuPDFBackend.EXTERNAL_DEPENDENCIES,
}


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in PyMuPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "png""',
                icon=str(icons_folder_path / 'png.ico'),
            ),
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "jpg""',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
        ])
    for ext in PDF2DOCXBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_docx",
                description="To DOCX",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "docx""',
                icon=str(icons_folder_path / 'docx.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_convert_cmd(
    input_files: List[Path],
    format: str,
    output_dir: Path,
    dpi: int = 200,
    password: str | None = None,
    progress_callback: Callable[[float], Any] = lambda p: p,
) -> None:
    with ProgressManager(len(input_files)) as progress_mgr:
        files = format_in_out_files_tuple(
            input_files=input_files,
            output_dir=output_dir,
            format=format,
        )
        logger.info(f"[bold]{_('Converting files')}[/] ...")
        # Perform conversion
        if format in PyMuPDFBackend.SUPPORTED_OUT_FORMATS:
            backend = PyMuPDFBackend(verbose=STATE['verbose'])
            for input_file, output_file in files:
                backend.convert(
                    input_file=input_file,
                    output_file=output_file,
                    dpi=dpi,
                    password=password,
                )
        else:
            backend = PDF2DOCXBackend(verbose=STATE['verbose'])
            for input_file, output_file in files:
                backend.convert(
                    input_file=input_file,
                    output_file=output_file,
                    password=password,
                )
        progress_callback(progress_mgr.complete_step())

    logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=CONVERT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a PDF file to a different format (might require LibreOffice).')}
        
        {_('Outputs a file with the PDF page number at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.pdf -f jpg --dpi 200`

        - `file_conversor -oo {COMMAND_NAME} {CONVERT_NAME} input_file.pdf -f png`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.pdf -f docx`
    """)
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(["pdf"])],
    format: Annotated[str, FormatOption({
        **PyMuPDFBackend.SUPPORTED_OUT_FORMATS,
        **PDF2DOCXBackend.SUPPORTED_OUT_FORMATS,
    })],
    dpi: Annotated[int, DPIOption()] = CONFIG["image-dpi"],
    password: Annotated[str | None, PasswordOption()] = None,
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_convert_cmd(
        input_files=input_files,
        format=format,
        dpi=dpi,
        password=password,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_convert_cmd",
]
