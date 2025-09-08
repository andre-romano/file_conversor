
# src\file_conversor\cli\ppt\convert_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import PPT_BACKEND

from file_conversor.cli.ppt._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Configuration, Environment, Log, State, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PPT_BACKEND.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # WordBackend commands
    for ext in PPT_BACKEND.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "{ext}"',
                icon=str(icons_folder_path / f"{ext}.ico"),
            )
            for ext in PPT_BACKEND.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CONVERT_NAME,
    help=f"""
        {_('Convert presentation files into other formats (requires Microsoft Word / LibreOffice).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.odp -o output_file.ppt`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.pptx -o output_file.pdf`
    """)
def convert(
    input_files: Annotated[List[str], InputFilesArgument(PPT_BACKEND)],
    format: Annotated[str, FormatOption(PPT_BACKEND)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    ppt_backend = PPT_BACKEND(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ppt_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")
    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
