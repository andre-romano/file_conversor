
# src\file_conversor\cli\pipeline\create_cmd.py

import typer

from typing import Annotated, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand

from file_conversor.backend import BatchBackend

from file_conversor.config import Configuration, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PipelineCreateTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = BatchBackend.EXTERNAL_DEPENDENCIES

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

    {_('Will ask questions interactively to create the file processing pipeline.')}

    {_('Placeholders available for commands')}:

    - **{{in_file_path}}**: {_('Replaced by the first file path found in pipeline stage.')}

        - Ex: C:/Users/Alice/Desktop/pipeline_name/my_file.jpg

    - **{{in_file_name}}**: {_('The name of the input file.')}

        - Ex: my_file

    - **{{in_file_ext}}**: {_('The extension of the input file.')}

        - Ex: jpg

    - **{{in_dir}}**: {_('The directory of the input path (previous pipeline stage).')}

        - Ex: C:/Users/Alice/Desktop/pipeline_name

    - **{{out_dir}}**: {_('The directory of the output path (current pipeline stage).')}

        - Ex: C:/Users/Alice/Desktop/pipeline_name/1_to_png
""",
            epilog=f"""
**{_('Examples')}:** 

- `file_conversor {group_name} {command_name}` 
""")

    def create(self):
        logger.info(f"{_('Creating batch pipeline')} ...")
        pipeline_folder: str = typer.prompt(f"{_('Name of the batch pipeline folder (e.g., %USERPROFILE%/Desktop/pipeline_name_here)')}")
        batch_backend = BatchBackend(pipeline_folder)

        terminate = False
        while not terminate:
            try:
                stage: str = typer.prompt(f"{_('Name of the processing stage (e.g., image_convert)')}")

                print(BatchBackend.StageConfigDataModel.help_template())
                cmd_str: str = typer.prompt(f"{_('Type command here')} ({_('e.g.')}, image convert {{in_file_path}} -od {{out_dir}} -f png )")
                batch_backend.pipeline.add_stage(stage, command=cmd_str)

                terminate = not typer.confirm(f"{_('Need another pipeline stage')}", default=False)
                print(f"-------------------------------------")
            except (KeyboardInterrupt, typer.Abort) as e:
                terminate = True
                raise
            except Exception as e:
                logger.error(f"{str(e)}")

        batch_backend.save_config()
        logger.info(f"{_('Pipeline creation')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PipelineCreateTyperCommand",
]
