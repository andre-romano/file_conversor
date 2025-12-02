
# src\file_conversor\cli\pdf\extract_img_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyMuPDFBackend

from file_conversor.cli.pdf._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, EXTRACT_IMG_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption


from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PyMuPDFBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in PyMuPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="extract_img",
                description="Extract IMG",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{EXTRACT_IMG_NAME}" "%1""',
                icon=str(icons_folder_path / 'separate.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_extract_img_cmd(
    input_files: List[Path],
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pymupdf_backend = PyMuPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pymupdf_backend.extract_images(
            # files
            input_file=input_file,
            output_dir=output_dir,
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=True)  # allow overwrite to avoid detecting PDF file as existing
    cmd_mgr.run(callback)

    logger.info(f"{_('Extract images')}: [bold green]{_('SUCCESS')}[/].")


# pdf extract-img
@typer_cmd.command(
    name=EXTRACT_IMG_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Extract images from a PDF.')}
        
        {_('For every PDF page, a new image file will be created using the format `input_file_X`, where X is the page number.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {EXTRACT_IMG_NAME} input_file.pdf -od D:/Downloads` 
    """)
def extract_img(
    input_files: Annotated[List[Path], InputFilesArgument(PyMuPDFBackend)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_extract_img_cmd(
        input_files=input_files,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_extract_img_cmd",
]
