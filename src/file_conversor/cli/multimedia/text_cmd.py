
# src\file_conversor\cli\multimedia\text_cmd.py

import typer

from typing import Annotated, List

from rich import print

# user-provided modules


from file_conversor.backend.text_backend import TextBackend
from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_valid_options

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
                command=f'{Environment.get_executable()} text convert "%1" -o "%1.xml"',
                icon=str(icons_folder_path / 'xml.ico'),
            ),
            WinContextCommand(
                name="to_json",
                description="To JSON",
                command=f'{Environment.get_executable()} text convert "%1" -o "%1.json"',
                icon=str(icons_folder_path / 'json.ico'),
            ),
            WinContextCommand(
                name="to_yaml",
                description="To YAML",
                command=f'{Environment.get_executable()} text convert "%1" -o "%1.yaml"',
                icon=str(icons_folder_path / 'yaml.ico'),
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

- `file_conversor hash convert file1.json -o file.xml` 
""")
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(TextBackend.SUPPORTED_IN_FORMATS)})",
    )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(TextBackend.SUPPORTED_OUT_FORMATS)}).",
                                             callback=lambda x: check_file_format(x, TextBackend.SUPPORTED_OUT_FORMATS)
                                             )],
):
    hash_backend = TextBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')}:", total=100,)
        hash_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress.update(task, total=100, completed=100)

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
    input_files: Annotated[List[str], typer.Argument(
        help=f"{_('Input file')} ({', '.join(TextBackend.SUPPORTED_IN_FORMATS)})",
    )],
):
    text_backend = TextBackend(verbose=STATE["verbose"])
    logger.info(f"{_('Checking files ...')}")

    # text_backend.check(
    #     input_files=input_files,
    # )

    logger.info(f"{_('Check')}: [bold green]{_('SUCCESS')}[/].")
