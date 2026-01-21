
# src\file_conversor\cli\image\info_cmd.py

from pathlib import Path
from typing import Annotated, Iterable, List

from rich import print
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import InputFilesArgument

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageInfoTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="info",
                    description="Get Info",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "info.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.info,
            help=f"""
    {_('Get EXIF information about a image file.')}

    {_('This command retrieves metadata and other information about the image file')}:
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} other_filename.jpg`

    - `file_conversor {group_name} {command_name} filename.webp filename2.png filename3.gif`
""")

    def info(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend.SUPPORTED_IN_FORMATS)],
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())
        for input_file in input_files:

            # 📁 Informações gerais do arquivo
            metadata = pillow_backend.info(input_file)
            input_name = input_file.name
            in_ext = input_file.suffix.upper()[1:]

            formatted = [
                f"{_('File Information')}:",
                f"  - {_('Name')}: {input_name}",
                f"  - {_('Format')}: {in_ext}",
            ]
            for tag, value in metadata.items():
                tag_name = PillowBackend.Exif_TAGS.get(tag, f"{tag}")
                formatted.append(f"  - {tag_name}: {value}")

            # Agrupar e exibir tudo com Rich
            group = Group(
                *formatted,
            )
            print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))


__all__ = [
    "ImageInfoTyperCommand",
]
