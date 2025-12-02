# src\file_conversor\cli\pipeline\__init__.py

import typer

# user-provided modules
from file_conversor.config import get_translation

from file_conversor.cli.pipeline._typer import COMMAND_NAME

from file_conversor.cli.pipeline.create_cmd import typer_cmd as create_cmd
from file_conversor.cli.pipeline.execute_cmd import typer_cmd as execute_cmd

_ = get_translation()

pipeline_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=f"""{_('Pipeline file processing (task automation)')}

                {_('The pipeline processsing by processing an input folder, passing those files to the next pipeline stage, and processing them inside that stage. This process continues (output of the current stage is the input of the next stage), until those files reach the end of the pipeline.')}



                {_('Example')}:

                - {_('Input folder')} => {_('Stage 1')} => {_('Stage 2')} => ... => {_('Output Folder')}
        """,
)
pipeline_cmd.add_typer(create_cmd)
pipeline_cmd.add_typer(execute_cmd)

__all__ = [
    "pipeline_cmd",
]
