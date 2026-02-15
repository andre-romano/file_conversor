
# src\file_conversor\cli\multimedia\filter_cmd.py
from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.image import ImageFilterCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageFilterCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageFilterCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # IMG2PDF commands
        for mode in ImageFilterCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="blur",
                    description="Blur",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" --filter blur"',
                    icon=str(icons_folder_path / "blur.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.filter,
            help=_('Applies filter to an image file.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads --filter blur`

    - `file_conversor {group_name} {command_name} input_file1.bmp -f sharpen`

    - `file_conversor {group_name} {command_name} input_file.jpg -f sharpen -f 3d`        
""")

    def filter(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageFilterCommand.SupportedInFormats)],
        filters: Annotated[list[ImageFilterCommand.PillowFilter], typer.Option("--filter", "-f",
                                                                               help=f'{_("Filter to apply. Available filters:")} {", ".join(mode.value for mode in ImageFilterCommand.PillowFilter)}',
                                                                               )],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageFilterCommand.filter(
                input_files=input_files,
                filters=filters,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageFilterCLI",
]
