
# src\file_conversor\cli\pdf\merge_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputFileOption,
    PasswordOption,
)
from file_conversor.command.pdf import PdfMergeCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfMergeCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfMergeCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.merge,
            help=f"""
    {_('Merge (join) input PDFs into a single PDF file.')}
    
    {_('Outputs a file with _merged at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Merge files "input_file1.pdf" and "input_file2.pdf" into "output_file.pdf"')}*:

    - `file_conversor {group_name} {command_name} "input_file1.pdf" "input_file2.pdf" -of output_file.pdf` 



    *{_('Merge protected PDFs "input_file1.pdf" and "input_file2.pdf" with password "unlock_password"')}*:

    - `file_conversor {group_name} {command_name} "input_file1.pdf" "input_file2.pdf" -p "unlock_password" -of output_file.pdf` 
""")

    def merge(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfMergeCommand.SupportedInFormats)],
        password: Annotated[str, PasswordOption()] = "",
        output_file: Annotated[Path | None, OutputFileOption(mode.value for mode in PdfMergeCommand.SupportedOutFormats)] = None,
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfMergeCommand.merge(
                input_files=input_files,
                password=password,
                output_file=output_file,
                progress_callback=task.update,
            )


__all__ = [
    "PdfMergeCLI",
]
