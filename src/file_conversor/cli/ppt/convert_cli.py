
# src\file_conversor\cli\ppt\convert_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.ppt import PptConvertCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PptConvertCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PptConvertCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # WordBackend commands
        for mode in PptConvertCommand.SupportedInFormats:
            ext_in = mode.value
            ctx_menu.add_extension(f".{ext_in}", [
                WinContextCommand(
                    name=f"to_{mode.value}",
                    description=f"To {mode.value.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f "{mode.value}" "%1""',
                    icon=str(icons_folder_path / f"{mode.value}.ico"),
                )
                for mode in PptConvertCommand.SupportedOutFormats
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=f"""
    {_('Convert presentation files into other formats (requires LibreOffice).')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.odp -o output_file.ppt`

    - `file_conversor {group_name} {command_name} input_file.pptx -o output_file.pdf`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PptConvertCommand.SupportedInFormats)],
        file_format: Annotated[PptConvertCommand.SupportedOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PptConvertCommand.convert(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PptConvertCLI",
]
