
# src\file_conversor\cli\multimedia\unsharp_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, RadiusOption

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageUnsharpTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # No context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.unsharp,
            help=_('Applies unsharp mask to an image file.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads`

    - `file_conversor {group_name} {command_name} input_file1.bmp -r 3`

    - `file_conversor {group_name} {command_name} input_file.jpg -s 100 -t 15`        
""")

    def unsharp(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],

        radius: Annotated[int, RadiusOption()] = 2,

        strength: Annotated[int, typer.Option("--strenght", "-s",
                                              help=f'{_("Unsharp strength, in percent")}',
                                              min=1,
                                              )] = 130,

        threshold: Annotated[int, typer.Option("--threshold", "-t",
                                               help=f'{_("Threshold controls the minimum brightness change that will be sharpened")}',
                                               min=1,
                                               )] = 4,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.unsharp_mask(
                input_file=input_file,
                output_file=output_file,
                radius=radius,
                percent=strength,
                threshold=threshold,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_unsharpened")

        logger.info(f"{_('Image unsharp')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageUnsharpTyperCommand",
]
