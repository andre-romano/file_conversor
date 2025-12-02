
# src\file_conversor\cli\pipeline\create_cmd.py

import typer

from typing import Annotated

from rich import print

# user-provided modules
from file_conversor.backend import BatchBackend

from file_conversor.cli.pipeline._typer import COMMAND_NAME, CREATE_NAME

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich_utils import get_progress_bar
from file_conversor.utils.validators import check_dir_exists

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = BatchBackend.EXTERNAL_DEPENDENCIES


# pipeline create
@typer_cmd.command(
    name=CREATE_NAME,
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

- `file_conversor {COMMAND_NAME} {CREATE_NAME}` 
""")
def create():
    logger.info(f"{_('Creating batch pipeline')} ...")
    pipeline_folder: str = typer.prompt(f"{_('Name of the batch pipeline folder (e.g., %USERPROFILE%/Desktop/pipeline_name_here)')}")
    batch_backend = BatchBackend(pipeline_folder)

    terminate = False
    while not terminate:
        try:
            stage: str = typer.prompt(f"{_('Name of the processing stage (e.g., image_convert)')}")

            cmd_str: str = typer.prompt(f"{_('Type command here')} ({_('e.g.')}, image convert {{in_file_path}} {{out_dir}}/{{in_file_name}}_converted.png )")
            batch_backend.add_stage(stage, command=cmd_str)

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
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
