
# src\file_conversor\cli\pipeline\execute_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Iterable

# user-provided modules

from file_conversor.cli._utils import AbstractTyperCommand, get_progress_bar

from file_conversor.backend import BatchBackend

from file_conversor.config import Configuration, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu

from file_conversor.utils.validators import check_dir_exists

# get app config
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PipelineExecuteTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = BatchBackend.EXTERNAL_DEPENDENCIES

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
        pipeline_folder: Annotated[Path, typer.Argument(
            help=f"{_('Pipeline folder')}",
            callback=lambda x: check_dir_exists(x),
        )],
    ):
        logger.info("Executing pipeline ...")
        batch_backend = BatchBackend(pipeline_folder)
        batch_backend.load_config()

        with get_progress_bar() as progress:
            total_stages = len(batch_backend.pipeline.stages)

            task_all_stages = progress.add_task(f"{_('Processing stage')}", total=total_stages)
            for i, stage in enumerate(batch_backend.pipeline.stages):
                task_stage = progress.add_task(description=f"{_('Processing stage')} {i + 1}/{total_stages}")
                stage.execute(lambda p, task_stage=task_stage: progress.update(task_stage, completed=p))
                progress.update(task_all_stages, completed=i + 1)

        logger.info(f"{_('Pipeline execution')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PipelineExecuteTyperCommand",
]
