
# src\file_conversor\cli\pipeline\execute_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.pipeline import PipelineExecuteCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu
from file_conversor.utils.validators import check_dir_exists


# get app config
STATE = State.get()
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PipelineExecuteCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PipelineExecuteCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        return  # No context menu for pipeline commands

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.execute,
            help=f"""
    {_('Execute file processing pipeline.')}        
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} c:/Users/Alice/Desktop/pipeline_name` 
""")

    def execute(
        self,
        pipeline_dir: Annotated[Path, typer.Argument(
            help=f"{_('Pipeline folder')}",
            callback=check_dir_exists,  # pyright: ignore[reportUnknownArgumentType]
        )],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PipelineExecuteCommand.execute(
                pipeline_dir=pipeline_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PipelineExecuteCLI",
]
