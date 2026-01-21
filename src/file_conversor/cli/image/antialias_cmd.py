
# src\file_conversor\cli\multimedia\antialias_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, RadiusOption

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


class ImageAntialiasTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # IMG2PDF commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
        radius: Annotated[int, RadiusOption()] = 3,
        algorithm: Annotated[PillowBackend.AntialiasAlgorithm, typer.Option("--algorithm", "-a",
                                                                            help=f'{_("Algorithm to use. Available algorihtms:")} {", ".join(mode.value for mode in PillowBackend.AntialiasAlgorithm)}.',
                                                                            )] = PillowBackend.AntialiasAlgorithm.MEDIAN,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.antialias(
                input_file=input_file,
                output_file=output_file,
                radius=radius,
                algorithm=algorithm,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_antialiased")

        logger.info(f"{_('Image antialiasing')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageAntialiasTyperCommand",
]
