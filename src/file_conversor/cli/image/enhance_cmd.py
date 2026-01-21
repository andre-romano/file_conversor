
# src\file_conversor\cli\multimedia\enhance_cmd.py
import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.abstract_typer_command import AbstractTyperCommand
from file_conversor.cli._utils.typer import BrightnessOption, ColorOption, ContrastOption, InputFilesArgument, OutputDirOption, SharpnessOption


from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.validators import is_close

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageEnhanceTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # IMG2PDF commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],

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

        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.enhance(
                input_file=input_file,
                output_file=output_file,
                color_factor=color,
                brightness_factor=brightness,
                contrast_factor=contrast,
                sharpness_factor=sharpness,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_enhanced")

        logger.info(f"{_('Image enhance')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageEnhanceTyperCommand",
]
