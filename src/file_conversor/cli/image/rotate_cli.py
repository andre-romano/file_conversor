
# src\file_conversor\cli\image\rotate_cli.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.image import ImageRotateCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu
from file_conversor.utils.formatters import normalize_degree


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageRotateCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageRotateCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for mode in ImageRotateCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="rotate_anticlock_90",
                    description="Rotate Left",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r -90"',
                    icon=str(icons_folder_path / "rotate_left.ico"),
                ),
                WinContextCommand(
                    name="rotate_clock_90",
                    description="Rotate Right",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r 90"',
                    icon=str(icons_folder_path / "rotate_right.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.rotate,
            help=f"""
    {_('Rotate a image file (clockwise or anti-clockwise).')}

    {_('Outputs an image file with _rotated at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads -r 90`

    - `file_conversor {group_name} {command_name} input_file.jpg -r -90 -o`
""")

    def rotate(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageRotateCommand.SupportedInFormats)],
        rotation: Annotated[int, typer.Option("--rotation", "-r",
                                              help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise rotation) and 360 (clockwise rotation)."),
                                              min=-360, max=360,
                                              )],

        resampling: Annotated[ImageRotateCommand.ResamplingOption, typer.Option("--resampling", "-re",
                                                                                help=f'{_("Resampling algorithm. Valid values are")} {", ".join(mode.value for mode in ImageRotateCommand.ResamplingOption)}. {_("Defaults to")} {CONFIG.image_resampling}.',
                                                                                )] = ImageRotateCommand.ResamplingOption(CONFIG.image_resampling),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageRotateCommand.rotate(
                input_files=input_files,
                rotation=normalize_degree(rotation),
                resampling=resampling,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageRotateCLI",
]
