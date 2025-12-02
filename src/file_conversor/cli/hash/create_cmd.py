
# src\file_conversor\cli\hash\create_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend import HashBackend

from file_conversor.cli.hash._typer import COMMAND_NAME, CREATE_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import FormatOption, InputFilesArgument, OutputDirOption
from file_conversor.utils.validators import check_path_exists

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = HashBackend.EXTERNAL_DEPENDENCIES


def execute_hash_create_cmd(
    input_files: List[Path],
    output_file: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    if not STATE["overwrite-output"]:
        check_path_exists(output_file, exists=False)

    hash_backend = HashBackend(
        verbose=STATE["verbose"],
    )
    with ProgressManager() as progress_mgr:
        hash_backend.generate(
            input_files=input_files,
            output_file=output_file,
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p)),
        )
        progress_callback(progress_mgr.complete_step())

    logger.info(f"{_('Hash creation')}: [bold green]{_('SUCCESS')}[/].")


@typer_cmd.command(
    name=CREATE_NAME,
    help=f"""
        {_('Creates a hash file (.sha256, .sha1, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {CREATE_NAME} file1.jpg file2.pdf file3.exe -f sha256` 

- `file_conversor {COMMAND_NAME} {CREATE_NAME} file1.jpg file2.pdf -f sha1 -od D:/Downloads` 
""")
def create(
    input_files: Annotated[List[Path], InputFilesArgument()],
    format: Annotated[str, FormatOption(HashBackend)],
    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    output_file = output_dir / f"CHECKSUM.{format}"
    execute_hash_create_cmd(
        input_files=input_files,
        output_file=output_file,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_hash_create_cmd",
]
