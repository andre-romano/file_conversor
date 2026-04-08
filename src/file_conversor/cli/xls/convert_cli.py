
# src\file_conversor\cli\xls\convert_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.xls import XlsConvertCommand
from file_conversor.command.xls.convert_cmd import XlsConvertOutFormats
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class XlsConvertCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path) -> None:
        # WordBackend commands
        for ext_in in XlsConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-f", ext_out],
                    icon=icons_folder / f"{ext_out}.ico",
                )
                for ext_out in XlsConvertCommand.get_out_formats()
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=f"""
    {_('Convert spreadsheet files into other formats (requires LibreOffice).')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.ods -f xls`

    - `file_conversor {group_name} {command_name} input_file.xlsx -f pdf`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(XlsConvertCommand.get_in_formats())],
        file_format: Annotated[XlsConvertOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = XlsConvertCommand(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "XlsConvertCLI",
]
