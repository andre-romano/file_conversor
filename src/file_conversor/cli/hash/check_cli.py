
# src\file_conversor\cli\hash\check_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.command.hash import HashCheckCommand
from file_conversor.config import (
    LOG,
    STATE,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCheckCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in HashCheckCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="check",
                    description="Check",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'check.ico',
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.check,
            help=_('Checks a hash file (.sha256, .sha1, etc).'),
            epilog=f"""
**{_('Examples')}:** 

- `file_conversor {group_name} {command_name} file.sha256` 
- `file_conversor {group_name} {command_name} file.sha1 file.sha3_512` 
""")

    def check(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(HashCheckCommand.get_in_formats())],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = HashCheckCommand(
                input_files=input_files,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "HashCheckCLI",
]
