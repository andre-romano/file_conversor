
# src\file_conversor\cli\pdf\encrypt_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.pdf import PdfEncryptCommand
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


class PdfEncryptCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfEncryptCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfEncryptCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="encrypt",
                    description="Encrypt",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "padlock_locked.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.encrypt,
            help=f"""
    {_('Protect PDF file with a password (create encrypted PDF file).')}
    
    {_('Outputs a file with _encrypted at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads --owner-password 1234`

    - `file_conversor {group_name} {command_name} input_file.pdf -op 1234 --up 0000 -an -co`
""")

    def encrypt(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfEncryptCommand.SupportedInFormats)],
        owner_password: Annotated[str, typer.Option("--owner-password", "-op",
                                                    help=_("Owner password for encryption. Owner has ALL PERMISSIONS in the output PDF file."),
                                                    prompt=f"{_('Owner password for encryption (password will not be displayed, for your safety)')}",
                                                    hide_input=True,
                                                    )],

        permissions: Annotated[list[PdfEncryptCommand.EncryptionPermission], typer.Option("--permission", "-p",
                                                                                          help=_("User permissions for the encrypted PDF file. Can be used multiple times to add multiple permissions. If no permissions are specified, the user will have no permissions (read-only)."),
                                                                                          )] = [PdfEncryptCommand.EncryptionPermission.NONE],  # noqa: B006

        user_password: Annotated[str, typer.Option("--user-password", "-up",
                                                          help=f'{_("User password for encryption. User has ONLY THE PERMISSIONS specified in the arguments. Defaults to")} None {_("(user and owner password are the same).")}',
                                                          )] = "",

        decrypt_password: Annotated[str, typer.Option("--decrypt-password", "-dp",
                                                             help=f'{_("Decrypt password used to open protected file. Defaults to")} None {_("(do not decrypt).")}',
                                                             )] = "",

        algorithm: Annotated[PdfEncryptCommand.EncryptionAlgorithm, typer.Option("--algorithm", "-a",
                                                                                 help=f'{_("Encryption algorithm used. ")} {_(f"Defaults to")} {PdfEncryptCommand.EncryptionAlgorithm.AES_256.value}.',
                                                                                 )] = PdfEncryptCommand.EncryptionAlgorithm.AES_256,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfEncryptCommand.encrypt(
                input_files=input_files,
                owner_password=owner_password,
                user_password=user_password,
                decrypt_password=decrypt_password,
                permissions=permissions,
                algorithm=algorithm,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfEncryptCLI",
]
