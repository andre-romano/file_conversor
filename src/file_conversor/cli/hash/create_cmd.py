
# src\file_conversor\cli\hash\create_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.backend import HashBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu
from file_conversor.utils.validators import check_path_exists

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCreateCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = HashBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for create command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.create,
            help=_('Creates a hash file (.sha256, .sha1, etc).'),
            epilog=f"""
**{_('Examples')}:** 

- `file_conversor {group_name} {command_name} file1.jpg file2.pdf file3.exe -f sha256` 

- `file_conversor {group_name} {command_name} file1.jpg file2.pdf -f sha1 -od D:/Downloads` 
""")

    def create(
        self,
        input_files: Annotated[List[Path], InputFilesArgument()],
        format: Annotated[str, FormatOption(HashBackend)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        output_file = output_dir / f"CHECKSUM.{format}"
        if not STATE.overwrite_output.enabled:
            check_path_exists(output_file, exists=False)

        hash_backend = HashBackend(
            verbose=STATE.loglevel.get().is_verbose(),
        )
        with ProgressManagerRich() as progress_mgr:
            hash_backend.generate(
                input_files=input_files,
                output_file=output_file,
                progress_callback=progress_mgr.update_progress,
            )
            progress_mgr.complete_step()

        logger.info(f"{_('Hash creation')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "HashCreateCommand",
]
