
# src\file_conversor\cli\pdf\repair_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    PasswordOption,
)
from file_conversor.command.pdf import PdfRepairCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfRepairCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfRepairCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfRepairCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="repair",
                    description="Repair",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'repair.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.repair,
            help=f"""
    {_('Attempt to repair a corrupted PDF file.')}        
    
    {_('Outputs a file with _repaired at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads` 
""")

    def repair(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfRepairCommand.SupportedInFormats)],
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfRepairCommand.repair(
                input_files=input_files,
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfRepairCLI",
]
