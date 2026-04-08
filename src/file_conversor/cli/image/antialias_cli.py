
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
from file_conversor.command.image import ImageAntialiasAlgorithm, ImageAntialiasCommand
from file_conversor.config import (
    LOG,
    STATE,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageAntialiasCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # IMG2PDF commands
        for ext_in in ImageAntialiasCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="antialias",
                    description="Antialias",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / "diagonal_line.ico",
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
        input_files: Annotated[list[Path], InputFilesArgument(ImageAntialiasCommand.get_in_formats())],
        radius: Annotated[int, RadiusOption()] = 3,
        algorithm: Annotated[ImageAntialiasAlgorithm,
                             typer.Option("--algorithm", "-a",
                                          help=f'{_("Algorithm to use.")}',
                                          )] = ImageAntialiasAlgorithm.MEDIAN,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageAntialiasCommand(
                input_files=input_files,
                radius=radius,
                algorithm=algorithm,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageAntialiasCLI",
]
