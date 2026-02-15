
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
from file_conversor.command.image import ImageMirrorCommand
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


class ImageMirrorCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageMirrorCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for mode in ImageMirrorCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="mirror_x",
                    description="Mirror X axis",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -a x"',
                    icon=str(icons_folder_path / "left_right.ico"),
                ),
                WinContextCommand(
                    name="mirror_y",
                    description="Mirror Y axis",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -a y"',
                    icon=str(icons_folder_path / "up_down.ico"),
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageMirrorCommand.SupportedInFormats)],
        axis: Annotated[ImageMirrorCommand.MirrorAxis, AxisOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageMirrorCommand.mirror(
                input_files=input_files,
                axis=axis,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageMirrorCLI",
]
