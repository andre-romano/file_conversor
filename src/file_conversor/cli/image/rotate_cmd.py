
# src\file_conversor\cli\multimedia\image_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageRotateTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
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

    - `file_conversor {group_name} {command_name} input_file.jpg -r -180 -o`
""")

    def rotate(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
        rotation: Annotated[int, typer.Option("--rotation", "-r",
                                              help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise rotation) and 360 (clockwise rotation)."),
                                              min=-360, max=360,
                                              )],

        resampling: Annotated[PillowBackend.ResamplingOption, typer.Option("--resampling", "-re",
                                                                           help=f'{_("Resampling algorithm. Valid values are")} {", ".join(mode.value for mode in PillowBackend.ResamplingOption)}. {_("Defaults to")} {CONFIG.image_resampling}.',
                                                                           )] = PillowBackend.ResamplingOption(CONFIG.image_resampling),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.rotate(
                input_file=input_file,
                output_file=output_file,
                rotate=rotation,
                resampling=resampling,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_rotated")

        logger.info(f"{_('Image rotation')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageRotateTyperCommand",
]
