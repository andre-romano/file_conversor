
# src\file_conversor\cli\image\antialias_cli.py

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
from file_conversor.command.image import ImageAntialiasCommand
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


class ImageAntialiasCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageAntialiasCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # IMG2PDF commands
        for mode in ImageAntialiasCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="antialias",
                    description="Antialias",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r 3"',
                    icon=str(icons_folder_path / "diagonal_line.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.antialias,
            help=_('Applies antialias filter to an image file.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file1.bmp -r 5`

    - `file_conversor {group_name} {command_name} input_file.jpg -r 2 -a mode`        
""")

    def antialias(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageAntialiasCommand.SupportedInFormats)],
        radius: Annotated[int, RadiusOption()] = 3,
        algorithm: Annotated[ImageAntialiasCommand.AntialiasAlgorithm,
                             typer.Option("--algorithm", "-a",
                                          help=f'{_("Algorithm to use. Available algorihtms:")} {", ".join(mode.value for mode in ImageAntialiasCommand.AntialiasAlgorithm)}.',
                                          )] = ImageAntialiasCommand.AntialiasAlgorithm.MEDIAN,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageAntialiasCommand.antialias(
                input_files=input_files,
                radius=radius,
                algorithm=algorithm,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageAntialiasCLI",
]
