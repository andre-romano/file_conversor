
# src\file_conversor\cli\multimedia\unsharp_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    RadiusOption,
)
from file_conversor.command import ImageUnsharpCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageUnsharpCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageUnsharpCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # No context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.unsharp,
            help=_('Applies unsharp mask to an image file.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads`

    - `file_conversor {group_name} {command_name} input_file1.bmp -r 3`

    - `file_conversor {group_name} {command_name} input_file.jpg -s 100 -t 15`        
""")

    def unsharp(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageUnsharpCommand.SupportedInFormats)],

        radius: Annotated[int, RadiusOption()] = 2,

        strength: Annotated[int, typer.Option("--strenght", "-s",
                                              help=f'{_("Unsharp strength, in percent")}',
                                              min=1,
                                              )] = 130,

        threshold: Annotated[int, typer.Option("--threshold", "-t",
                                               help=f'{_("Threshold controls the minimum brightness change that will be sharpened")}',
                                               min=1,
                                               )] = 4,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageUnsharpCommand.unsharp(
                input_files=input_files,
                radius=radius,
                strength=strength,
                threshold=threshold,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageUnsharpCLI",
]
