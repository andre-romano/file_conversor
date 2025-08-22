
# src\file_conversor\cli\utils\batch_cmd.py

import typer

from typing import Annotated

from rich import print

# user-provided modules
from file_conversor.backend.batch_backend import BatchBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

batch_cmd = typer.Typer()


# batch create
@batch_cmd.command(
    help=f"""
        {_('Creates a batch file processing pipeline (for tasks automation).')}        

        {_('Will ask questions interactively to create a batch file processing pipeline.')}

        [bold]{_('Placeholders available for commands')}[/]:

        - [bold]{{in_file_path}}[/]: {_('Replaced by the first file path found in pipeline stage.')}

            - Ex: C:/Users/Alice/Desktop/pipeline_name/my_file.jpg

        - [bold]{{in_file_name}}[/]: {_('The name of the input file.')}

            - Ex: my_file

        - [bold]{{in_file_ext}}[/]: {_('The extension of the input file.')}

            - Ex: jpg

        - [bold]{{in_dir}}[/]: {_('The directory of the input path (previous pipeline stage).')}

            - Ex: C:/Users/Alice/Desktop/pipeline_name

        - [bold]{{out_dir}}[/]: {_('The directory of the output path (current pipeline stage).')}

            - Ex: C:/Users/Alice/Desktop/pipeline_name/1_to_png
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor batch create` 
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
    logger.info(f"{_('Batch creation')}: [bold green]{_('SUCCESS')}[/].")


# batch execute
@batch_cmd.command(
    help=f"""
        {_('Execute batch file processing pipeline.')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor batch execute c:/Users/Alice/Desktop/pipeline_name` 
""")
def execute(
    pipeline_folder: Annotated[str, typer.Argument(
        help=f"{_('Pipeline folder')}",
    )],
):
    logger.info("Executing batch pipeline ...")
    with get_progress_bar() as progress:
        batch_backend = BatchBackend(pipeline_folder)
        batch_backend.load_config()
        batch_backend.execute(progress)

    logger.info(f"{_('Batch execution')}: [bold green]{_('SUCCESS')}[/].")
    logger.info(f"--------------------------------")
