
# src\file_conversor\cli\multimedia\text_cmd.py

import typer

from pathlib import Path

from rich import print


# user-provided modules
from file_conversor.backend import TextBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils import ProgressManager, CommandManager

from file_conversor.utils.validators import *
from file_conversor.utils.typer import *

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

text_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in TextBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_xml",
                description="To XML",
                command=f'{Environment.get_executable()} text convert "%1" -f "xml"',
                icon=str(icons_folder_path / 'xml.ico'),
            ),
            WinContextCommand(
                name="to_json",
                description="To JSON",
                command=f'{Environment.get_executable()} text convert "%1" -f "json"',
                icon=str(icons_folder_path / 'json.ico'),
            ),
            WinContextCommand(
                name="to_yaml",
                description="To YAML",
                command=f'{Environment.get_executable()} text convert "%1" -f "yaml"',
                icon=str(icons_folder_path / 'yaml.ico'),
            ),
            WinContextCommand(
                name="to_toml",
                description="To TOML",
                command=f'{Environment.get_executable()} text convert "%1" -f "toml"',
                icon=str(icons_folder_path / 'toml.ico'),
            ),
            WinContextCommand(
                name="to_ini",
                description="To INI",
                command=f'{Environment.get_executable()} text convert "%1" -f "ini"',
                icon=str(icons_folder_path / 'ini.ico'),
            ),
            WinContextCommand(
                name="check",
                description="Check",
                command=f'cmd /k "{Environment.get_executable()} text check "%1""',
                icon=str(icons_folder_path / 'check.ico'),
            ),
            WinContextCommand(
                name="compress",
                description="Compress",
                command=f'{Environment.get_executable()} text compress "%1"',
                icon=str(icons_folder_path / 'compress.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# text convert
@text_cmd.command(
    help=f"""
        {_('Converts text file formats (json, xml, yaml, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor text convert file1.json -f xml` 
""")
def convert(
    input_files: InputFilesArgument(TextBackend),  # pyright: ignore[reportInvalidTypeForm]
    format: FormatOption(TextBackend),  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    text_backend = TextBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_suffix=f".{format}")
    logger.info(f"{_('File conversion')}: [bold green]{_('SUCCESS')}[/].")


# text check
@text_cmd.command(
    help=f"""
        {_('Checks a text file (json, xml, yaml, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor text check file.json` 

- `file_conversor text check file1.json file2.yaml` 
""")
def check(
    input_files: InputFilesArgument(TextBackend),  # pyright: ignore[reportInvalidTypeForm]
):
    text_backend = TextBackend(verbose=STATE["verbose"])
    logger.info(f"{_('Checking files')} ...")

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.check(
            input_file=input_file,
        )
    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite"])
    cmd_mgr.run(callback)
    logger.info(f"{_('Check')}: [bold green]{_('SUCCESS')}[/].")


# text compress
@text_cmd.command(
    help=f"""
        {_('Compress / minify text file formats (json, xml, yaml, etc).')}        
        
        {_('Outputs a file with .min at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor hash compress file1.json` 
""")
def compress(
    input_files: InputFilesArgument(TextBackend),  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    text_backend = TextBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.minify(
            input_file=input_file,
            output_file=output_file,
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem=f"_compressed")
    logger.info(f"{_('Compression')}: [bold green]{_('SUCCESS')}[/].")
