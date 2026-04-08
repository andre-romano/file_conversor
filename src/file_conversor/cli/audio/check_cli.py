
# src\file_conversor\cli\audio\check_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.command.audio import AudioCheckCommand
from file_conversor.config import (
    LOG,
    STATE,
    get_translation,
)
from file_conversor.system.context_menu import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioCheckCLI(AbstractTyperCommand):
    """Audio check command class."""
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # FFMPEG commands
        for ext_in in AudioCheckCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="check",
                    description="Check",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'check.ico',
                    keep_terminal_open=True,
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.check,
            help=_("Checks audio files for corruption / inconsistencies."),
            epilog=f"""
**{_('Examples')}:** 

- `file_conversor {group_name} {command_name} input_file.mp3`
""",
        )

    def check(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(AudioCheckCommand.get_in_formats())],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = AudioCheckCommand(
                input_files=input_files,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "AudioCheckCLI",
]
