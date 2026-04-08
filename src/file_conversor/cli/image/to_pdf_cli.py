
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
from file_conversor.command.image import (
    ImageToPdfCommand,
    ImageToPdfFitMode,
    ImageToPdfPageLayout,
)
from file_conversor.config import CONFIG, LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.utils.formatters import get_output_file
from file_conversor.utils.validators import check_is_bool_or_none


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageToPdfCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in ImageToPdfCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="to_pdf",
                    description="To PDF",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / "pdf.ico",
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
        input_files: Annotated[list[Path], InputFilesArgument(ImageToPdfCommand.get_in_formats())],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        fit: Annotated[ImageToPdfFitMode, typer.Option("--fit", "-f",
                                                       help=f"{_("Image fit. Valid only if")} --page-size {_("is defined.")}",
                                                       )] = ImageToPdfFitMode(CONFIG.image_fit),
        page_size: Annotated[ImageToPdfPageLayout, typer.Option("--page-size", "-ps",
                                                                help=f"{_("Page size.")} {_("Defaults to")} None ({_("PDF size = image size")}).",
                                                                )] = ImageToPdfPageLayout(CONFIG.image_page_size),
        set_metadata: Annotated[bool, typer.Option("--set-metadata", "-sm",
                                                   help=_("Set PDF metadata. Defaults to False (do not set creator, producer, modification date, etc)."),
                                                   callback=check_is_bool_or_none,
                                                   is_flag=True,
                                                   )] = False,

        output_file: Annotated[Path | None, OutputFileOption(ImageToPdfCommand.get_out_formats())] = None,
    ):
        if not output_file:
            output_file = get_output_file(
                input_file=input_files[0] if input_files else Path("output"),
                out_suffix=".pdf",
            )

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageToPdfCommand(
                input_files=input_files,
                dpi=dpi,
                fit=fit,
                page_size=page_size,
                set_metadata=set_metadata,
                output_file=output_file,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageToPdfCLI",
]
