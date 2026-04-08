
# src\file_conversor\cli\pdf\split_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    PasswordOption,
)
from file_conversor.command.pdf import PdfSplitCommand
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfSplitCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in PdfSplitCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="split",
                    description="Split",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'split.ico',
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.split,
            help=f"""
    {_('Split PDF pages into several 1-page PDFs.')}

    {_('For every PDF page, a new single page PDF will be created using the format `input_file_X.pdf`, where X is the page number.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Split pages of input_file.pdf into output_file_X.pdf files')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads` 



    *{_('For every PDF page, generate a "input_file_X.pdf" file')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf` 
""")

    def split(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(PdfSplitCommand.get_in_formats())],
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = PdfSplitCommand(
                input_files=input_files,
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "PdfSplitCLI",
]
