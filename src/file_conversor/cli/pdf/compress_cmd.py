
# src\file_conversor\cli\pdf\compress_cmd.py

import tempfile
import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PikePDFBackend, GhostscriptBackend

from file_conversor.cli.pdf._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, COMPRESS_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption
from file_conversor.utils.validators import check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = {
    *PikePDFBackend.EXTERNAL_DEPENDENCIES,
    *GhostscriptBackend.EXTERNAL_DEPENDENCIES,
}


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in GhostscriptBackend.SUPPORTED_IN_FORMATS:
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


def execute_pdf_compress_cmd(
    input_files: List[Path],
    compression: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pikepdf_backend = PikePDFBackend(verbose=STATE["verbose"])
    gs_backend = GhostscriptBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE['verbose'],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        with tempfile.TemporaryDirectory() as temp_dir:
            gs_out = Path(temp_dir) / CommandManager.get_output_file(input_file, stem="_gs")
            gs_backend.compress(
                input_file=input_file,
                output_file=gs_out,
                compression_level=GhostscriptBackend.Compression.from_str(compression),
                progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
            )
            progress_callback(progress_mgr.complete_step())

            pikepdf_backend.compress(
                # files
                input_file=gs_out,
                output_file=output_file,
                progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p))
            )
            progress_callback(progress_mgr.complete_step())
            print(f"Processing '{output_file}' ... OK")

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, steps=2, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_compressed")

    logger.info(f"{_('File compression')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=COMPRESS_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Reduce the file size of a PDF document (requires Ghostscript external library).')}
        
        {_('Outputs a file with _compressed at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file.pdf -od D:/Downloads`

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file.pdf -c high`

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file.pdf -o`
    """)
def compress(
    input_files: Annotated[List[Path], InputFilesArgument(GhostscriptBackend)],
    compression: Annotated[str, typer.Option("--compression", "-c",
                                             help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(GhostscriptBackend.Compression.get_dict())}. {_('Defaults to')} {CONFIG["pdf-compression"]}.",
                                             callback=lambda x: check_valid_options(x, GhostscriptBackend.Compression.get_dict()),
                                             )] = CONFIG["pdf-compression"],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_compress_cmd(
        input_files=input_files,
        compression=compression,
        output_dir=output_dir,
    )

    logger.info(f"{_('File compression')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_compress_cmd",
]
