
# src\file_conversor\cli\multimedia\image_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.cli.image._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, ROTATE_NAME

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

EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # Pillow commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="rotate_anticlock_90",
                description="Rotate Left",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r -90"',
                icon=str(icons_folder_path / "rotate_left.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_90",
                description="Rotate Right",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{ROTATE_NAME}" "%1" -r 90"',
                icon=str(icons_folder_path / "rotate_right.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_rotate_cmd(
    input_files: List[Path],
    rotation: int,
    resampling: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.rotate(
            input_file=input_file,
            output_file=output_file,
            rotate=rotation,
            resampling=PillowBackend.RESAMPLING_OPTIONS[resampling],
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_rotated")

    logger.info(f"{_('Image rotation')}: [green bold]{_('SUCCESS')}[/]")


@typer_cmd.command(
    name=ROTATE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Rotate a image file (clockwise or anti-clockwise).')}

        {_('Outputs an image file with _rotated at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {ROTATE_NAME} input_file.jpg -od D:/Downloads -r 90`

        - `file_conversor {COMMAND_NAME} {ROTATE_NAME} input_file.jpg -r -180 -o`
    """)
def rotate(
    input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
    rotation: Annotated[int, typer.Option("--rotation", "-r",
                                          help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise rotation) and 360 (clockwise rotation)."),
                                          min=-360, max=360,
                                          )],

    resampling: Annotated[str, typer.Option("--resampling", "-re",
                                            help=f'{_("Resampling algorithm. Valid values are")} {", ".join(PillowBackend.RESAMPLING_OPTIONS)}. {_("Defaults to")} {CONFIG["image-resampling"]}.',
                                            callback=lambda x: check_valid_options(x, PillowBackend.RESAMPLING_OPTIONS),
                                            )] = CONFIG["image-resampling"],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_rotate_cmd(
        input_files=input_files,
        rotation=rotation,
        resampling=resampling,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_rotate_cmd",
]
