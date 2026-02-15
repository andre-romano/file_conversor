
# src\file_conversor\cli\hash\create_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.hash import HashCreateCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCreateCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = HashCreateCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for create command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.create,
            help=_('Creates a hash file (.sha256, .sha1, etc).'),
            epilog=f"""
**{_('Examples')}:** 

- `file_conversor {group_name} {command_name} file1.jpg file2.pdf file3.exe -f sha256` 

- `file_conversor {group_name} {command_name} file1.jpg file2.pdf -f sha1 -od D:/Downloads` 
""")

    def create(
        self,
        input_files: Annotated[list[Path], InputFilesArgument()],
        file_format: Annotated[HashCreateCommand.SupportedOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            HashCreateCommand.create(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "HashCreateCLI",
]
