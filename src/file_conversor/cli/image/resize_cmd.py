
# src\file_conversor\cli\multimedia\image_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.cli.image._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, RESIZE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager

from file_conversor.utils.formatters import parse_image_resize_scale
from file_conversor.utils.typer_utils import InputFilesArgument, OutputDirOption
from file_conversor.utils.validators import check_positive_integer, check_valid_options

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
                name="resize",
                description="Resize",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{RESIZE_NAME}" "%1""',
                icon=str(icons_folder_path / "resize.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_image_resize_cmd(
    input_files: List[Path],
    scale: float | None,
    width: int | None,
    resampling: str,
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])

    scale = parse_image_resize_scale(scale, width, quiet=STATE["quiet"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        pillow_backend.resize(
            input_file=input_file,
            output_file=output_file,
            scale=scale,
            width=width,
            resampling=PillowBackend.RESAMPLING_OPTIONS[resampling],
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_resized")

    logger.info(f"{_('Image resize')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=RESIZE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Resize an image file.')}

        {_('Outputs an image file with _resized at the end.')}
""",
    epilog=f"""
        **{_('Examples')}:**



        *{_('Double the image size')}*:

        - `file_conversor {COMMAND_NAME} {RESIZE_NAME} input_file.jpg -s 2.0`



        *{_('Set the image width to 1024px')}*:

        - `file_conversor {COMMAND_NAME} {RESIZE_NAME} input_file.jpg -od D:/Downloads -w 1024`
    """)
def resize(
    input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
    scale: Annotated[float | None, typer.Option("--scale", "-s",
                                                help=f"{_("Scale image proportion. Valid values start at 0.1. Defaults to")} None (use width to scale image).",
                                                callback=lambda x: check_positive_integer(x),
                                                )] = None,

    width: Annotated[int | None, typer.Option("--width", "-w",
                                              help=f"{_("Width in pixels (height is calculated based on width to keep image proportions). Defaults to")} None ({_('use scale to resize image')}).",
                                              callback=lambda x: check_positive_integer(x),
                                              )] = None,

    resampling: Annotated[str, typer.Option("--resampling", "-r",
                                            help=f'{_("Resampling algorithm. Valid values are")} {", ".join(PillowBackend.RESAMPLING_OPTIONS)}. {_("Defaults to")} {CONFIG["image-resampling"]}.',
                                            callback=lambda x: check_valid_options(x, PillowBackend.RESAMPLING_OPTIONS),
                                            )] = CONFIG["image-resampling"],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_image_resize_cmd(
        input_files=input_files,
        scale=scale,
        width=width,
        resampling=resampling,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_image_resize_cmd",
]
