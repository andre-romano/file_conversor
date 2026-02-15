
# src\file_conversor\cli\image\to_pdf_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    DPIOption,
    InputFilesArgument,
    OutputFileOption,
)
from file_conversor.command.image import ImageToPdfCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu
from file_conversor.utils.formatters import get_output_file
from file_conversor.utils.validators import check_is_bool_or_none


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageToPdfCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageToPdfCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # IMG2PDF commands
        for mode in ImageToPdfCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_pdf",
                    description="To PDF",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "pdf.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.to_pdf,
            help=f"""
    {_('Convert a list of image files to one PDF file, one image per page.')}

    Fit = {_('Valid only if ``--page-size`` is defined. Otherwise, PDF size = figure size.')}

    - 'into': {_('Figure adjusted to fit in PDF size')}.

    - 'fill': {_('Figure adjusted to fit in PDF size')}, {_('without any empty borders (cut figure if needed)')}.
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -of output_file.pdf --dpi 96`

    - `file_conversor {group_name} {command_name} input_file1.bmp input_file2.png -of output_file.pdf`

    - `file_conversor {group_name} {command_name} input_file.jpg -of output_file.pdf -ps a4_landscape`
""")

    def to_pdf(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageToPdfCommand.SupportedInFormats)],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        fit: Annotated[ImageToPdfCommand.FitMode, typer.Option("--fit", "-f",
                                                               help=f"{_("Image fit. Valid only if")} --page-size {_("is defined.")} {_("Defaults to")} {CONFIG.image_fit}",
                                                               )] = ImageToPdfCommand.FitMode(CONFIG.image_fit),
        page_size: Annotated[ImageToPdfCommand.PageLayout, typer.Option("--page-size", "-ps",
                                                                        help=f"{_("Page size.")} {_("Defaults to")} None ({_("PDF size = image size")}).",
                                                                        )] = ImageToPdfCommand.PageLayout(CONFIG.image_page_size),
        set_metadata: Annotated[bool, typer.Option("--set-metadata", "-sm",
                                                   help=_("Set PDF metadata. Defaults to False (do not set creator, producer, modification date, etc)."),
                                                   callback=check_is_bool_or_none,
                                                   is_flag=True,
                                                   )] = False,

        output_file: Annotated[Path | None, OutputFileOption(mode.value for mode in ImageToPdfCommand.SupportedOutFormats)] = None,
    ):
        if not output_file:
            output_file = get_output_file(
                input_file=input_files[0] if input_files else Path("output"),
                out_suffix=".pdf",
            )

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageToPdfCommand.to_pdf(
                input_files=input_files,
                dpi=dpi,
                fit=fit,
                page_size=page_size,
                set_metadata=set_metadata,
                output_file=output_file,
                progress_callback=task.update,
            )


__all__ = [
    "ImageToPdfCLI",
]
