
# src\file_conversor\cli\video\check_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument

from file_conversor.backend import FFprobeBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoCheckTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFprobeBackend.SUPPORTED_IN_VIDEO_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="check",
                    description="Check",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'check.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.check,
            help=_('Checks a audio/video file for corruption / inconsistencies.'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm`
""")

    def check(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend)],
    ):
        # init ffmpeg
        backend = FFprobeBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            # display current progress
            try:
                backend.info(input_file)
                progress_mgr.complete_step()
            except Exception as e:
                logger.error(f"{_('Error checking file')} '{input_file}': {e}")

        cmd_mgr = CommandManagerRich(input_files, output_dir=Path(), overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback)

        logger.info(f"{_('FFMpeg check')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "VideoCheckTyperCommand",
]
