# src\file_conversor\cli\__init__.py

import sys
import typer

from rich import print

from pathlib import Path
from typing import Annotated, Any

# user-provided imports
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation

from file_conversor.cli._typer import COMMANDS_LIST, PYTHON_VERSION

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()

# Create a Typer CLI application
app_cmd = typer.Typer(
    rich_markup_mode="markdown",
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
    }
)


#####################
# REGISTER COMMANDS #
#####################

for cmd_obj in COMMANDS_LIST:
    app_cmd.add_typer(**cmd_obj)


#####################
#     APP PANEL
#####################


def version_callback(value: bool):
    if value:
        VERSION = Environment.get_version()
        print(f"File Conversor {VERSION}")
        print(f"Python {PYTHON_VERSION} ({sys.executable})")
        raise typer.Exit()


# Main callback, to process global options
@app_cmd.callback(
    help=f"""
        # File Conversor - CLI
    """,
    epilog=f"""
        {_('For more information, visit')} [http://www.github.com/andre-romano/file_conversor](http://www.github.com/andre-romano/file_conversor)
    """)
def main_callback(
        no_log: Annotated[bool, typer.Option(
            "--no-log", "-nl",
            help=_("Disable file logs"),
            is_flag=True,
        )] = False,
        no_progress: Annotated[bool, typer.Option(
            "--no-progress", "-np",
            help=f"{_('Disable progress bars')}",
            is_flag=True,
        )] = False,
        quiet: Annotated[bool, typer.Option(
            "--quiet", "-q",
            help=f"{_('Enable quiet mode (only display errors and progress bars)')}",
            is_flag=True,
        )] = False,
        verbose: Annotated[bool, typer.Option(
            "--verbose", "-v",
            help=_("Enable verbose mode"),
            is_flag=True,
        )] = False,
        debug: Annotated[bool, typer.Option(
            "--debug", "-d",
            help=_("Enable debug mode"),
            is_flag=True,
        )] = False,
        version: Annotated[bool, typer.Option(
            "--version", "-V",
            help=_("Display version"),
            callback=version_callback,
            is_flag=True,
        )] = False,
        overwrite_output: Annotated[bool, typer.Option(
            "--overwrite-output", "-oo",
            help=f"{_('Overwrite output files')}. Defaults to False (do not overwrite).",
            is_flag=True,
        )] = False,
):
    STATE.update({
        "no-log": no_log,
        "no-progress": no_progress,
        "quiet": quiet,
        "verbose": verbose,
        "debug": debug,
        "overwrite-output": overwrite_output,
    })
    logger.debug(f"Python {PYTHON_VERSION} ({sys.executable})")
    logger.debug(f"Command: {sys.argv}")
    # Environment.get_executable()
    logger.debug(f"Working directory: {Path().resolve()}")
    logger.debug(f"Resources folder: {Environment.get_resources_folder()}")
    logger.debug(f"Data folder: {Environment.get_data_folder()}")
    logger.debug(f"Available languages: {sorted(AVAILABLE_LANGUAGES)} ({len(AVAILABLE_LANGUAGES)} entries)")
    logger.debug(f"Language (config / sys): ({CONFIG['language']} / {get_system_locale()})")


__all__ = [
    "app_cmd",
]
