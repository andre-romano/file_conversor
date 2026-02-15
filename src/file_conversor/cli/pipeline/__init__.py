# src\file_conversor\cli\pipeline\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.cli.pipeline.create_cli import PipelineCreateCLI
from file_conversor.cli.pipeline.execute_cli import PipelineExecuteCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class PipelineTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CREATE = "create"
        EXECUTE = "execute"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=f"""
    {_('Pipeline file processing (task automation)')}

    {_('The pipeline processsing by processing an input folder, passing those files to the next pipeline stage, and processing them inside that stage. This process continues (output of the current stage is the input of the next stage), until those files reach the end of the pipeline.')}



    {_('Example')}:

    - {_('Input folder')} => {_('Stage 1')} => {_('Stage 2')} => ... => {_('Output Folder')}
""",
        )

        # add subcommands
        self.add(
            PipelineCreateCLI(
                group_name=group_name,
                command_name=self.Commands.CREATE.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            PipelineExecuteCLI(
                group_name=group_name,
                command_name=self.Commands.EXECUTE.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "PipelineTyperGroup",
]
