
# src\file_conversor\cli\text\convert_cmd.py

import typer

from typing import Annotated, Any, Callable, List
from pathlib import Path

from rich import print


# user-provided modules
from file_conversor.backend import TextBackend

from file_conversor.cli.text._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption


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
                name="to_xml",
                description="To XML",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "xml""',
                icon=str(icons_folder_path / 'xml.ico'),
            ),
            WinContextCommand(
                name="to_json",
                description="To JSON",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "json""',
                icon=str(icons_folder_path / 'json.ico'),
            ),
            WinContextCommand(
                name="to_yaml",
                description="To YAML",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "yaml""',
                icon=str(icons_folder_path / 'yaml.ico'),
            ),
            WinContextCommand(
                name="to_toml",
                description="To TOML",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "toml""',
                icon=str(icons_folder_path / 'toml.ico'),
            ),
            WinContextCommand(
                name="to_ini",
                description="To INI",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "ini""',
                icon=str(icons_folder_path / 'ini.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_text_convert_cmd(
    input_files: List[Path],
    format: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    text_backend = TextBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")
    logger.info(f"{_('File conversion')}: [bold green]{_('SUCCESS')}[/].")


# text convert
@typer_cmd.command(
    name=CONVERT_NAME,
    help=f"""
        {_('Converts text file formats (json, xml, yaml, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {CONVERT_NAME} file1.json -f xml` 
""")
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(TextBackend)],
    format: Annotated[str, FormatOption(TextBackend)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_text_convert_cmd(
        input_files=input_files,
        format=format,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_text_convert_cmd",
]
