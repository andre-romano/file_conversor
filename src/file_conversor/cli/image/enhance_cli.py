
# src\file_conversor\cli\image\enhance_cli.py
from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    BrightnessOption,
    ColorOption,
    ContrastOption,
    InputFilesArgument,
    OutputDirOption,
    SharpnessOption,
)
from file_conversor.command.image import ImageEnhanceCommand
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


class ImageEnhanceCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageEnhanceCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in ImageEnhanceCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="enhance",
                    description="Enhance",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "color.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.enhance,
            help=_('Enhance image color, brightness, contrast, or sharpness.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads --color 1.20`

    - `file_conversor {group_name} {command_name} input_file1.bmp --sharpness 0.85`

    - `file_conversor {group_name} {command_name} input_file.jpg -cl 0.85 -b 1.10`        
""")

    def enhance(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageEnhanceCommand.SupportedInFormats)],

        brightness: Annotated[float, BrightnessOption()] = 1.00,
        contrast: Annotated[float, ContrastOption()] = 1.00,
        color: Annotated[float, ColorOption()] = 1.00,
        sharpness: Annotated[float, SharpnessOption()] = 1.00,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if is_close(brightness, 1.00) and is_close(contrast, 1.00) and is_close(color, 1.00) and is_close(sharpness, 1.00):
            brightness = typer.prompt("Brightness factor (> 1.0 increases, < 1.0 decreases)", default=1.00)
            contrast = typer.prompt("Contrast factor (> 1.0 increases, < 1.0 decreases)", default=1.00)
            color = typer.prompt("Color factor (> 1.0 increases, < 1.0 decreases)", default=1.00)
            sharpness = typer.prompt("Sharpness factor (> 1.0 increases, < 1.0 decreases)", default=1.00)

        if brightness < 0.0 or contrast < 0.0 or color < 0.0 or sharpness < 0.0:
            raise ValueError(_("Enhancement factors must be greater than 0.0"))

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageEnhanceCommand.enhance(
                input_files=input_files,
                brightness=brightness,
                contrast=contrast,
                color=color,
                sharpness=sharpness,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageEnhanceCLI",
]
