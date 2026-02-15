
# src\file_conversor\cli\audio\check_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.command.audio import AudioCheckCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioCheckCLI(AbstractTyperCommand):
    """Audio check command class."""
    EXTERNAL_DEPENDENCIES = AudioCheckCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for mode in AudioCheckCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="check",
                    description="Check",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'check.ico'),
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in AudioCheckCommand.SupportedInFormats)],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            AudioCheckCommand.check(
                input_files=input_files,
                progress_callback=task.update,
            )


__all__ = [
    "AudioCheckCLI",
]
