
# src\file_conversor\cli\pdf\repair_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PikePDFBackend

from file_conversor.cli.pdf._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, REPAIR_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PikePDFBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in PikePDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="repair",
                description="Repair",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{REPAIR_NAME}" "%1"',
                icon=str(icons_folder_path / 'repair.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=REPAIR_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Repair (lightly) corrupted PDF files.')}        
        
        {_('Outputs a file with _repaired at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {REPAIR_NAME} input_file.pdf -od D:/Downloads` 
""")
def repair(
    input_files: Annotated[List[str], InputFilesArgument(PikePDFBackend)],
    password: Annotated[str | None, PasswordOption()] = None,
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    pikepdf_backend = PikePDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ... ")
        pikepdf_backend.compress(
            # files
            input_file=input_file,
            output_file=output_file,

            # options
            decrypt_password=password,
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_repaired")

    logger.info(f"{_('Repair PDF')}: [bold green]{_('SUCCESS')}[/].")
