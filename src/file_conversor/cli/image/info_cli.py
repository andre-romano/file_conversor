
# src\file_conversor\cli\image\info_cli.py

from pathlib import Path
from typing import Annotated, override

from rich import print
from rich.console import Group
from rich.panel import Panel

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.command.image import ImageInfoCommand
from file_conversor.config import LOG, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageInfoCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # Pillow commands
        for ext_in in ImageInfoCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="info",
                    description="Get Info",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / "info.ico",
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
        input_files: Annotated[list[Path], InputFilesArgument(ImageInfoCommand.get_in_formats())],
    ):
        command = ImageInfoCommand(input_files=input_files)
        command.execute()

        for input_file, metadata in command.output.items():
            # 📁 Informações gerais do arquivo
            input_name = input_file.name
            in_ext = input_file.suffix.upper()[1:]

            formatted = [
                f"{_('File Information')}:",
                f"  - {_('Name')}: {input_name}",
                f"  - {_('Format')}: {in_ext}",
            ]
            for tag_name, value in metadata.items():
                formatted.append(f"  - {tag_name}: {value}")

            # Agrupar e exibir tudo com Rich
            group = Group(
                *formatted,
            )
            print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))
        logger.info(f"{_('Image info')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageInfoCLI",
]
