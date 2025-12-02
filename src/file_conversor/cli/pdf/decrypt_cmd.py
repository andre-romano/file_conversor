
# src\file_conversor\cli\pdf\decrypt_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.cli.pdf._typer import SECURITY_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, DECRYPT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption

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
                name="decrypt",
                description="Decrypt",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{DECRYPT_NAME}" "%1""',
                icon=str(icons_folder_path / "padlock_unlocked.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_decrypt_cmd(
    input_files: List[Path],
    password: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.decrypt(
            input_file=input_file,
            output_file=output_file,
            password=password,
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_decrypted")
    logger.info(f"{_('Decryption')}: [bold green]{_('SUCCESS')}[/].")


# pdf decrypt
@typer_cmd.command(
    name=DECRYPT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Remove password protection from a PDF file  (create decrypted PDF file).')}        
        
        {_('Outputs a file with _decrypted at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {DECRYPT_NAME} input_file.pdf input_file2.pdf --password 1234`

        - `file_conversor {COMMAND_NAME} {DECRYPT_NAME} input_file.pdf -p 1234`
    """)
def decrypt(
    input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
    password: Annotated[str, typer.Option("--password", "-p",
                                          help=_("Password used for decryption."),
                                          prompt=f"{_('Password for decryption (password will not be displayed, for your safety)')}",
                                          hide_input=True,
                                          )],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_decrypt_cmd(
        input_files=input_files,
        password=password,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_decrypt_cmd",
]
