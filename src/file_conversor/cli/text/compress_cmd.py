
# src\file_conversor\cli\text\compress_cmd.py

import typer

from typing import Annotated, Any, Callable, List
from pathlib import Path

from rich import print


# user-provided modules
from file_conversor.backend import TextBackend

from file_conversor.cli.text._typer import COMMAND_NAME, COMPRESS_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption


# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in TextBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="compress",
                description="Compress",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{COMPRESS_NAME}" "%1""',
                icon=str(icons_folder_path / 'compress.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_text_compress_cmd(
    input_files: List[Path],
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    text_backend = TextBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.minify(
            input_file=input_file,
            output_file=output_file,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem=f"_compressed")
    logger.info(f"{_('Compression')}: [bold green]{_('SUCCESS')}[/].")


# text compress
@typer_cmd.command(
    name=COMPRESS_NAME,
    help=f"""
        {_('Compress / minify text file formats (json, xml, yaml, etc).')}        
        
        {_('Outputs a file with .min at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {COMPRESS_NAME} file1.json` 
""")
def compress(
    input_files: Annotated[List[Path], InputFilesArgument(TextBackend)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_text_compress_cmd(
        input_files=input_files,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_text_compress_cmd",
]
