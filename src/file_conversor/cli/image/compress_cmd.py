
# src\file_conversor\cli\image\compress_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.image import CompressBackend

from file_conversor.cli.image._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, COMPRESS_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption, QualityOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = CompressBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # compress commands
    for ext in CompressBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="compress",
                description="Compress",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{COMPRESS_NAME}" "%1" -q 90"',
                icon=str(icons_folder_path / 'compress.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_compress_cmd(
    input_files: List[Path],
    quality: int,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    compress_backend = CompressBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        compress_backend.compress(
            input_file=input_file,
            output_file=output_file,
            quality=quality,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_compressed")

    logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=COMPRESS_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Compress an image file (requires external libraries).')}

        {_('Outputs an image file with _compressed at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file.jpg -q 85`

        - `file_conversor {COMMAND_NAME} {COMPRESS_NAME} input_file.png -od D:/Downloads -o`
    """)
def compress(
    input_files: Annotated[List[Path], InputFilesArgument(CompressBackend)],
    quality: Annotated[int, QualityOption()] = CONFIG["image-quality"],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_compress_cmd(
        input_files=input_files,
        quality=quality,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_compress_cmd",
]
