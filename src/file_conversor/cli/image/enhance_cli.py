
# src\file_conversor\cli\image\enhance_cli.py
from pathlib import Path
from typing import Annotated, override

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
    LOG,
    STATE,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.utils.validators import is_close, prompt_retry_on_exception


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageEnhanceCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in ImageEnhanceCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="enhance",
                    description="Enhance",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / "color.ico",
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
        input_files: Annotated[list[Path], InputFilesArgument(ImageEnhanceCommand.get_in_formats())],

        brightness: Annotated[float, BrightnessOption()] = 1.00,
        contrast: Annotated[float, ContrastOption()] = 1.00,
        color: Annotated[float, ColorOption()] = 1.00,
        sharpness: Annotated[float, SharpnessOption()] = 1.00,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if all(is_close(x, 1.00) for x in [brightness, contrast, color, sharpness]):
            brightness = prompt_retry_on_exception(
                "Brightness factor (> 1.0 increases, < 1.0 decreases)",
                type=float, default=1.00,
                callback=lambda x: x > 0.0,
            )
            contrast = prompt_retry_on_exception(
                "Contrast factor (> 1.0 increases, < 1.0 decreases)",
                type=float, default=1.00,
                callback=lambda x: x > 0.0,
            )
            color = prompt_retry_on_exception(
                "Color factor (> 1.0 increases, < 1.0 decreases)",
                type=float, default=1.00,
                callback=lambda x: x > 0.0,
            )
            sharpness = prompt_retry_on_exception(
                "Sharpness factor (> 1.0 increases, < 1.0 decreases)",
                type=float, default=1.00,
                callback=lambda x: x > 0.0,
            )

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageEnhanceCommand(
                input_files=input_files,
                brightness=brightness,
                contrast=contrast,
                color=color,
                sharpness=sharpness,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageEnhanceCLI",
]
