
# src\file_conversor\cli\pdf\extract_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    PasswordOption,
)
from file_conversor.command.pdf import PdfExtractCommand
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.utils.formatters import parse_pdf_pages
from file_conversor.utils.validators import prompt_retry_on_exception


_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfExtractCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in PdfExtractCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="extract",
                    description="Extract",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'extract.ico',
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.extract,
            help=f"""
    {_('Extract specific pages from a PDF.')}
    
    {_('Outputs a file with _extracted at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Extract pages 1 to 2, and 4')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf -pg 1-2 -pg 4 -od D:/Downloads` 
""")

    def extract(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(PdfExtractCommand.get_in_formats())],
        pages: Annotated[list[str] | None, typer.Option("--pages", "-pg",
                                                        help=_('Pages to extract (comma-separated list). Format "start-end".'),
                                                        )] = None,
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if not pages:
            pages_str = prompt_retry_on_exception(
                f"{_('Pages to extract [comma-separated list] (e.g., 1-3, 7-7)')}",
                type=str,
            )
            pages = [p.strip() for p in pages_str.split(",")]

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = PdfExtractCommand(
                input_files=input_files,
                pages=parse_pdf_pages(pages),
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "PdfExtractCLI",
]
