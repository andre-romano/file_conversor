
# src\file_conversor\cli\pdf\encrypt_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.cli.pdf._typer import SECURITY_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, ENCRYPT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption
from file_conversor.utils.validators import check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in PyPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="encrypt",
                description="Encrypt",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{ENCRYPT_NAME}" "%1""',
                icon=str(icons_folder_path / "padlock_locked.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_encrypt_cmd(
    input_files: List[Path],

    decrypt_password: str | None,

    owner_password: str,
    user_password: str | None,

    permissions: Iterable[PyPDFBackend.EncryptionPermission] | None,

    encrypt_algo: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.encrypt(
            # files
            input_file=input_file,
            output_file=output_file,

            # passwords
            owner_password=owner_password,
            user_password=user_password,
            decrypt_password=decrypt_password,

            # permissions
            permissions=permissions,

            encryption_algorithm=PyPDFBackend.EncryptionAlgorithm.from_str(encrypt_algo),
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_encrypted")
    logger.info(f"{_('Encryption')}: [bold green]{_('SUCCESS')}[/].")


@typer_cmd.command(
    name=ENCRYPT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Protect PDF file with a password (create encrypted PDF file).')}
        
        {_('Outputs a file with _encrypted at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {ENCRYPT_NAME} input_file.pdf -od D:/Downloads --owner-password 1234`

        - `file_conversor {COMMAND_NAME} {ENCRYPT_NAME} input_file.pdf -op 1234 --up 0000 -an -co`
    """)
def encrypt(
    input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
    owner_password: Annotated[str, typer.Option("--owner-password", "-op",
                                                help=_("Owner password for encryption. Owner has ALL PERMISSIONS in the output PDF file."),
                                                prompt=f"{_('Owner password for encryption (password will not be displayed, for your safety)')}",
                                                hide_input=True,
                                                )],

    permissions: Annotated[List[PyPDFBackend.EncryptionPermission], typer.Option("--permission", "-p",
                                                                                 help=_("User permissions for the encrypted PDF file. Can be used multiple times to add multiple permissions. If no permissions are specified, the user will have no permissions (read-only)."),
                                                                                 )] = [PyPDFBackend.EncryptionPermission.NONE],

    user_password: Annotated[str | None, typer.Option("--user-password", "-up",
                                                      help=_("User password for encryption. User has ONLY THE PERMISSIONS specified in the arguments. Defaults to None (user and owner password are the same)."),
                                                      )] = None,

    decrypt_password: Annotated[str | None, typer.Option("--decrypt-password", "-dp",
                                                         help=_("Decrypt password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,

    algorithm: Annotated[str, typer.Option("--algorithm", "-a",
                                           help=_("Encryption algorithm used. Valid options are RC4-40, RC4-128, AES-128, AES-256-R5, or AES-256. Defaults to AES-256 (for enhanced security and compatibility)."),
                                           callback=lambda x: check_valid_options(x, valid_options=PyPDFBackend.EncryptionAlgorithm.get_dict()),
                                           )] = PyPDFBackend.EncryptionAlgorithm.AES_256.value,

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_encrypt_cmd(
        input_files=input_files,
        decrypt_password=decrypt_password,
        owner_password=owner_password,
        user_password=user_password,
        permissions=permissions,
        encrypt_algo=algorithm,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_encrypt_cmd",
]
