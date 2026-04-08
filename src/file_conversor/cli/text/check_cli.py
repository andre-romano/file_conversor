
# src\file_conversor\cli\text\check_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.command.text import TextCheckCommand
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class TextCheckCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in TextCheckCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="check",
                    description="Check",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'check.ico',
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.check,
            help=_('Checks a text file schema compliance (json, xml, yaml, etc).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} file.json` 

    - `file_conversor {group_name} {command_name} file1.json file2.yaml` 
""")

    def check(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(TextCheckCommand.get_in_formats())],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = TextCheckCommand(
                input_files=input_files,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "TextCheckCLI",
]
