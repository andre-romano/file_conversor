
# src\file_conversor\cli\image\mirror_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AxisOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.image import ImageMirrorAxis, ImageMirrorCommand
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageMirrorCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # Pillow commands
        for ext_in in ImageMirrorCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="mirror_x",
                    description="Mirror X axis",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-a", "x"],
                    icon=icons_folder / "left_right.ico",
                ),
                ContextMenuItem(
                    name="mirror_y",
                    description="Mirror Y axis",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-a", "y"],
                    icon=icons_folder / "up_down.ico",
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.mirror,
            help=f"""
    {_('Mirror an image file (vertically or horizontally).')}

    {_('Outputs an image file with _mirrored at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads -a x`

    - `file_conversor {group_name} {command_name} input_file.png -a y -o`
""")

    def mirror(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(ImageMirrorCommand.get_in_formats())],
        axis: Annotated[ImageMirrorAxis, AxisOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageMirrorCommand(
                input_files=input_files,
                axis=axis,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageMirrorCLI",
]
