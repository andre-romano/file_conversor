
# src\file_conversor\cli\doc\convert_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import DOC_BACKEND

from file_conversor.cli.doc._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption


from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = DOC_BACKEND.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # WordBackend commands
    for ext in DOC_BACKEND.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "{ext}"',
                icon=str(icons_folder_path / f"{ext}.ico"),
            )
            for ext in DOC_BACKEND.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CONVERT_NAME,
    help=f"""
        {_('Convert document files into other formats (requires Microsoft Office / LibreOffice).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.odt -f doc`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.docx -f pdf`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.pdf -f docx`
    """)
def convert(
    input_files: Annotated[List[str], InputFilesArgument(DOC_BACKEND)],
    format: Annotated[str, FormatOption(DOC_BACKEND)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):

    files: list[tuple[Path | str, Path | str]] = []
    for input_file in input_files:
        output_file = output_dir / CommandManager.get_output_file(input_file, suffix=f".{format}")
        if not STATE["overwrite-output"] and output_file.exists():
            raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")
        files.append((input_file, output_file))

    doc_backend = DOC_BACKEND(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    with ProgressManager(len(input_files)) as progress_mgr:
        logger.info(f"[bold]{_('Converting files')}[/] ...")
        # Perform conversion
        doc_backend.convert(
            files=files,
            file_processed_callback=lambda _: progress_mgr.complete_step()
        )

    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
