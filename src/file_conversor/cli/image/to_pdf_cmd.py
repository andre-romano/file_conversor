
# src\file_conversor\cli\image\to_pdf_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.image import Img2PDFBackend

from file_conversor.cli.image._typer import CONVERSION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, TO_PDF_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import DPIOption, InputFilesArgument, OutputFileOption
from file_conversor.utils.validators import check_is_bool_or_none, check_path_exists, check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = Img2PDFBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # IMG2PDF commands
    for ext in Img2PDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_pdf",
                description="To PDF",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{TO_PDF_NAME}" "%1""',
                icon=str(icons_folder_path / "pdf.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_to_pdf_cmd(
    input_files: List[Path],
    dpi: int,
    fit: Img2PDFBackend.FitMode,
    page_size: Img2PDFBackend.PageLayout | None,
    set_metadata: bool,
    output_file: Path | None,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    output_file = output_file if output_file else Path() / CommandManager.get_output_file(input_files[0], suffix=".pdf")
    if not STATE.overwrite_output.enabled:
        check_path_exists(output_file, exists=False)

    img2pdf_backend = Img2PDFBackend(verbose=STATE.loglevel.get().is_verbose())
    # display current progress
    with ProgressManager() as progress_mgr:
        page_sz = page_size.get() if page_size else None

        img2pdf_backend.to_pdf(
            input_files=input_files,
            output_file=output_file,
            dpi=dpi,
            image_fit=fit,
            page_size=page_sz,
            include_metadata=set_metadata,
        )
        progress_callback(progress_mgr.complete_step())
    logger.info(f"{_('PDF generation')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=TO_PDF_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a list of image files to one PDF file, one image per page.')}

        Fit = {_('Valid only if ``--page-size`` is defined. Otherwise, PDF size = figure size.')}

        - 'into': {_('Figure adjusted to fit in PDF size')}.

        - 'fill': {_('Figure adjusted to fit in PDF size')}, {_('without any empty borders (cut figure if needed)')}.
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {TO_PDF_NAME} input_file.jpg -of output_file.pdf --dpi 96`

        - `file_conversor {COMMAND_NAME} {TO_PDF_NAME} input_file1.bmp input_file2.png -of output_file.pdf`

        - `file_conversor {COMMAND_NAME} {TO_PDF_NAME} input_file.jpg -of output_file.pdf -ps a4_landscape`
    """)
def to_pdf(
    input_files: Annotated[List[Path], InputFilesArgument(Img2PDFBackend)],
    dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
    fit: Annotated[Img2PDFBackend.FitMode, typer.Option("--fit", "-f",
                                                        help=f"{_("Image fit. Valid only if ``--page-size`` is defined. Valid values are")} {", ".join(mode.value for mode in Img2PDFBackend.FitMode)}. {_("Defaults to")} {CONFIG.image_fit}",
                                                        )] = Img2PDFBackend.FitMode(CONFIG.image_fit),
    page_size: Annotated[Img2PDFBackend.PageLayout | None, typer.Option("--page-size", "-ps",
                                                                        help=f"{_("Page size. Valid values are:")} {", ".join(mode.value for mode in Img2PDFBackend.PageLayout)}. {_("Defaults to None (PDF size = image size).")}",
                                                                        )] = Img2PDFBackend.PageLayout(CONFIG.image_page_size) if CONFIG.image_page_size else None,
    set_metadata: Annotated[bool, typer.Option("--set-metadata", "-sm",
                                               help=_("Set PDF metadata. Defaults to False (do not set creator, producer, modification date, etc)."),
                                               callback=check_is_bool_or_none,
                                               is_flag=True,
                                               )] = False,

    output_file: Annotated[Path | None, OutputFileOption(Img2PDFBackend)] = None,
):
    execute_image_to_pdf_cmd(
        input_files=input_files,
        dpi=dpi,
        fit=fit,
        page_size=page_size,
        set_metadata=set_metadata,
        output_file=output_file,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_to_pdf_cmd",
]
