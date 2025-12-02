
# src\file_conversor\cli\multimedia\typer_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List
from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.cli.image._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, MIRROR_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import AxisOption, InputFilesArgument, OutputDirOption
from file_conversor.utils.validators import check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # Pillow commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="mirror_x",
                description="Mirror X axis",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{MIRROR_NAME}" "%1" -a x"',
                icon=str(icons_folder_path / "left_right.ico"),
            ),
            WinContextCommand(
                name="mirror_y",
                description="Mirror Y axis",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{MIRROR_NAME}" "%1" -a y"',
                icon=str(icons_folder_path / "up_down.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_mirror_cmd(
    input_files: List[Path],
    axis: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.mirror(
            input_file=input_file,
            output_file=output_file,
            x_y=True if axis == "x" else False,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_mirrored")
    logger.info(f"{_('Image mirroring')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=MIRROR_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Mirror an image file (vertically or horizontally).')}

        {_('Outputs an image file with _mirrored at the end.')}
""",
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {MIRROR_NAME} input_file.jpg -od D:/Downloads -a x`

        - `file_conversor {COMMAND_NAME} {MIRROR_NAME} input_file.png -a y -o`
    """)
def mirror(
    input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
    axis: Annotated[str, AxisOption()],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_mirror_cmd(
        input_files=input_files,
        axis=axis,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_mirror_cmd",
]
