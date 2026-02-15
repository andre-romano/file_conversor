
# src\file_conversor\cli\pdf\decrypt_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.pdf import PdfDecryptCommand
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


class PdfDecryptCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfDecryptCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfDecryptCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="decrypt",
                    description="Decrypt",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "padlock_unlocked.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.decrypt,
            help=f"""
    {_('Remove password protection from a PDF file  (create decrypted PDF file).')}        
    
    {_('Outputs a file with _decrypted at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf input_file2.pdf --password 1234`

    - `file_conversor {group_name} {command_name} input_file.pdf -p 1234`
""")

    def decrypt(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfDecryptCommand.SupportedInFormats)],
        password: Annotated[str, typer.Option("--password", "-p",
                                              help=_("Password used for decryption."),
                                              prompt=f"{_('Password for decryption (password will not be displayed, for your safety)')}",
                                              hide_input=True,
                                              )],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfDecryptCommand.decrypt(
                input_files=input_files,
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfDecryptCLI",
]
