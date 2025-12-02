
# src\file_conversor\cli\ebook\convert_cmd.py

import typer

from rich import print

from typing import Annotated, Any, Callable, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import CalibreBackend

from file_conversor.cli.ebook._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = CalibreBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in CalibreBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "{ext}""',
                icon=str(icons_folder_path / f"{ext}.ico"),
            )
            for ext in CalibreBackend.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_ebook_convert_cmd(
    input_files: List[Path],
    format: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
) -> None:
    """Execute ebook conversion command."""
    calibre_backend = CalibreBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        calibre_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=CONVERT_NAME,
    help=f"""
        {_('Convert an ebook file to another ebook format (or PDF).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.epub -f pdf -od output_dir/`
        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.mobi -f epub`
    """)
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(CalibreBackend.SUPPORTED_IN_FORMATS)],

    format: Annotated[str, FormatOption(CalibreBackend.SUPPORTED_OUT_FORMATS)],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_ebook_convert_cmd(
        input_files=input_files,
        format=format,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_ebook_convert_cmd",
]
