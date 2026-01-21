
# src\file_conversor\cli\pdf\decrypt_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules

from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfDecryptTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in PyPDFBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
        password: Annotated[str, typer.Option("--password", "-p",
                                              help=_("Password used for decryption."),
                                              prompt=f"{_('Password for decryption (password will not be displayed, for your safety)')}",
                                              hide_input=True,
                                              )],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            pypdf_backend.decrypt(
                input_file=input_file,
                output_file=output_file,
                password=password,
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_decrypted")
        logger.info(f"{_('Decryption')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfDecryptTyperCommand",
]
