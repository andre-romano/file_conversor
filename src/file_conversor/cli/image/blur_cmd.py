
# src\file_conversor\cli\multimedia\blur_cmd.py
from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, RadiusOption

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageBlurTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        return

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.blur,
            help=_('Applies gaussian blur to an image file.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads`

    - `file_conversor {group_name} {command_name} input_file1.bmp -r 3`
""")

    def blur(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
        radius: Annotated[int, RadiusOption()] = 3,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.blur(
                input_file=input_file,
                output_file=output_file,
                blur_pixels=radius,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_blurred")

        logger.info(f"{_('Image blur')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageBlurTyperCommand",
]
