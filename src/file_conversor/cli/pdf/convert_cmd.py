
# src\file_conversor\cli\pdf\convert_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyMuPDFBackend, PDF2DOCXBackend

from file_conversor.cli.pdf._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, CONVERT_NAME

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

EXTERNAL_DEPENDENCIES = set([
    *PyMuPDFBackend.EXTERNAL_DEPENDENCIES,
    *PDF2DOCXBackend.EXTERNAL_DEPENDENCIES,
])


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in PyMuPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "png"',
                icon=str(icons_folder_path / 'png.ico'),
            ),
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "jpg"',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
        ])
    # pdf2docx
    for ext in PDF2DOCXBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_docx",
                description="To DOCX",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "docx"',
                icon=str(icons_folder_path / 'docx.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CONVERT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a PDF file to a different format.')}        
        
        {_('Outputs a file with the PDF page number at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.pdf -f jpg --dpi 200`

        - `file_conversor -oo {COMMAND_NAME} {CONVERT_NAME} input_file.pdf -f png`
    """)
def convert(
    input_files: Annotated[List[str], InputFilesArgument(["pdf"])],
    format: Annotated[str, FormatOption({
        **PyMuPDFBackend.SUPPORTED_OUT_FORMATS,
        **PDF2DOCXBackend.SUPPORTED_OUT_FORMATS,
    })],
    dpi: Annotated[int, DPIOption()] = CONFIG["image-dpi"],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    pymupdf_backend = PyMuPDFBackend(verbose=STATE['verbose'])
    pdf2docx_backend = PDF2DOCXBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ...")
        if format in PDF2DOCXBackend.SUPPORTED_OUT_FORMATS:
            pdf2docx_backend.to_docx(
                input_file=input_file,
                output_file=output_file,
            )
        elif format in PyMuPDFBackend.SUPPORTED_OUT_FORMATS:
            pymupdf_backend.convert(
                input_file=input_file,
                output_file=output_file,
                dpi=dpi,
            )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
