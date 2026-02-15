
# src\file_conversor\cli\pipeline\create_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.pipeline import PipelineCreateCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
STATE = State.get()
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PipelineCreateCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PipelineCreateCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        return  # No context menu for pipeline commands

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.create,
            help=f"""
    {_('Creates a file processing pipeline (for tasks automation).')}        

    {_('Placeholders available for commands')}:

    {PipelineCreateCommand.help()}
""",
            epilog=f"""
**{_('Examples')}:** 

- `file_conversor {group_name} {command_name} pipeline_name_here --stage 'image convert {{in_file}} -od {{out_dir}} -f png' --stage 'image compress {{in_file}} -od {{out_dir}}' ` 
""")

    def create(
        self,
        pipeline_dir: Annotated[Path, typer.Argument(
            help=_("Path to the folder where the pipeline configuration will be created."),
        )],
        stages: Annotated[list[str], typer.Option("--stage", "-s",
                                                  help=_("Processing stage command in the pipeline. E.g. image convert {in_file} -od {out_dir} -f png."),
                                                  )],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PipelineCreateCommand.create(
                pipeline_dir=pipeline_dir,
                stages=stages,
                progress_callback=task.update,
            )


__all__ = [
    "PipelineCreateCLI",
]
