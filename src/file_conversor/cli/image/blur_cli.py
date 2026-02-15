
# src\file_conversor\cli\image\blur_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    RadiusOption,
)
from file_conversor.command.image import ImageBlurCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageBlurCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageBlurCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        return

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.blur,
            help=_('Applies gaussian blur to an image file.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads`

    - `file_conversor {group_name} {command_name} input_file1.bmp -r 3`
""")

    def blur(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageBlurCommand.SupportedInFormats)],
        radius: Annotated[int, RadiusOption()] = 3,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageBlurCommand.blur(
                input_files=input_files,
                radius=radius,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageBlurCLI",
]
