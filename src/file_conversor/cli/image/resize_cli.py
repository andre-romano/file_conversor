
# src\file_conversor\cli\image\resize_cli.py

from pathlib import Path
from typing import Annotated, override

import typer

# CLI
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

# COMMAND
from file_conversor.command.image import ImageResizeCommand

# CORE
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu
from file_conversor.utils.validators import is_close


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageResizeCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageResizeCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for mode in ImageResizeCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="resize",
                    description="Resize",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "resize.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.resize,
            help=f"""
    {_('Resize an image file.')}

    {_('Outputs an image file with _resized at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:**



    *{_('Double the image size')}*:

    - `file_conversor {group_name} {command_name} input_file.jpg -s 2.0`



    *{_('Set the image width to 1024px')}*:

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads -w 1024`
""")

    def resize(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageResizeCommand.SupportedInFormats)],
        scale: Annotated[float, typer.Option("--scale", "-s",
                                             help=f"{_("Scale image proportion. Valid values start at 0.1. Defaults to")} 0 (use width to scale image).",
                                             min=0.0,
                                             )] = 0.0,

        width: Annotated[int, typer.Option("--width", "-w",
                                           help=f"{_("Width in pixels (height is calculated based on width to keep image proportions). Defaults to")} 0 ({_('use scale to resize image')}).",
                                           min=0,
                                           )] = 0,

        resampling: Annotated[ImageResizeCommand.ResamplingOption, typer.Option("--resampling", "-r",
                                                                                help=f'{_("Resampling algorithm. Valid values are")} {", ".join(mode.value for mode in ImageResizeCommand.ResamplingOption)}. {_("Defaults to")} {CONFIG.image_resampling}.',
                                                                                )] = ImageResizeCommand.ResamplingOption(CONFIG.image_resampling),
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if is_close(scale, 0.0) and width == 0:
            if STATE.loglevel.get().is_quiet():
                raise RuntimeError(f"{_('Scale and width not provided')}")
            scale = float(typer.prompt(f"{_('Output image scale (e.g., 1.5)')}", type=float))

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageResizeCommand.resize(
                input_files=input_files,
                scale=scale,
                width=width,
                resampling=resampling,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageResizeCLI",
]
