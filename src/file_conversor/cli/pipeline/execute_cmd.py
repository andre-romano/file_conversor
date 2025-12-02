
# src\file_conversor\cli\pipeline\execute_cmd.py

import typer

from typing import Annotated

from rich import print

# user-provided modules
from file_conversor.backend import BatchBackend

from file_conversor.cli.pipeline._typer import COMMAND_NAME, EXECUTE_NAME

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


@typer_cmd.command(
    name=EXECUTE_NAME,
    help=f"""
        {_('Execute file processing pipeline.')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {EXECUTE_NAME} c:/Users/Alice/Desktop/pipeline_name` 
""")
def execute(
    pipeline_folder: Annotated[str, typer.Argument(
        help=f"{_('Pipeline folder')}",
        callback=check_dir_exists
    )],
):
    logger.info("Executing pipeline ...")
    with get_progress_bar() as progress:
        batch_backend = BatchBackend(pipeline_folder)
        batch_backend.load_config()
        batch_backend.execute(progress)

    logger.info(f"{_('Pipeline execution')}: [bold green]{_('SUCCESS')}[/].")
    logger.info(f"--------------------------------")


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
