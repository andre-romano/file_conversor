
# src\file_conversor\cli\doc_cmd.py

import re
import time
import typer

from pathlib import Path
from typing import Annotated, List, Optional

from rich import print

# user-provided modules
from file_conversor.backend import Docx2PDFBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
doc_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = State.get_icons_folder()
    # Docx2PDFBackend commands
    for ext in Docx2PDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_pdf",
                description="To PDF",
                command=f'{State.get_executable()} doc to-pdf "%1"',
                icon=str(icons_folder_path / "pdf.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# doc to-pdf
@doc_cmd.command(
    help=f"""
        {_('Convert DOCX file into PDF file (requires Microsoft Word or MacOSx).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor doc to-pdf input_file.docx`

        - `file_conversor doc to-pdf input_file.docx -o output_file.pdf`
    """)
def to_pdf(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(Docx2PDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, Docx2PDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],

    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(Docx2PDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}).",
                                                    callback=lambda x: check_file_format(None, Docx2PDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
):
    docx2pdf_backend = Docx2PDFBackend()

    logger.info(f"{_('Processing file')} '{input_file}' ...")

    output_file = output_file if output_file else f"{input_file.replace(".pdf", "")}.pdf"
    docx2pdf_backend.to_pdf(
        input_file=input_file,
        output_file=output_file,
    )

    logger.info(f"{_('PDF generation')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
