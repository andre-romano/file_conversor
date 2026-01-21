
# src\file_conversor\cli\image\convert_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption, QualityOption

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageConvertTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_jpg",
                    description="To JPG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "jpg" -q 90"',
                    icon=str(icons_folder_path / 'jpg.ico'),
                ),
                WinContextCommand(
                    name="to_png",
                    description="To PNG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "png" -q 90"',
                    icon=str(icons_folder_path / 'png.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert a image file to a different format.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.webp -f jpg --quality 85`

    - `file_conversor {group_name} {command_name} input_file.bmp -f png -od D:/Downloads`
""")

    def convert(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
        file_format: Annotated[str, FormatOption(PillowBackend)],
        quality: Annotated[int, QualityOption()] = CONFIG.image_quality,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.convert(
                input_file=input_file,
                output_file=output_file,
                quality=quality,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_suffix=f".{file_format}")

        logger.info(f"{_('Image convertion')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageConvertTyperCommand",
]
