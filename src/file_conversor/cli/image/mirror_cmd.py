
# src\file_conversor\cli\multimedia\typer_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import AxisOption, InputFilesArgument, OutputDirOption

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageMirrorTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
        axis: Annotated[str, AxisOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.mirror(
                input_file=input_file,
                output_file=output_file,
                x_y=True if axis == "x" else False,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_mirrored")
        logger.info(f"{_('Image mirroring')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageMirrorTyperCommand",
]
