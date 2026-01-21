# src\file_conversor\cli\__init__.py

import sys
import typer

from pathlib import Path
from typing import Annotated, Any

# user-provided imports
from file_conversor.cli._typer import PYTHON_VERSION, get_commands

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation

# Get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

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

for cmd_obj in get_commands():
    app_cmd.add_typer(cmd_obj)


#####################
#     APP PANEL
#####################


def version_callback(value: bool):
    if not value:
        return
    VERSION = Environment.get_version()
    logger.info(f"File Conversor {VERSION}")
    logger.info(f"Python {PYTHON_VERSION} ({sys.executable})")
    raise typer.Exit()


def self_test_callback(value: bool):
    if not value:
        return

    try:
        # show version info
        version_callback(True)
    except typer.Exit:
        pass

    from file_conversor.config.self_tests import SelfTests
    SelfTests().run_self_tests()

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
        self_test: Annotated[bool, typer.Option(
            "--self-test", "-st",
            help=_("Run self tests"),
            callback=self_test_callback,
            is_flag=True,
        )] = False,
        overwrite_output: Annotated[bool, typer.Option(
            "--overwrite-output", "-oo",
            help=f"{_('Overwrite output files')}. Defaults to False (do not overwrite).",
            is_flag=True,
        )] = False,
):
    STATE.overwrite_output.enabled = overwrite_output
    STATE.logfile.enabled = not no_log
    STATE.progress.enabled = not no_progress
    if quiet:
        STATE.loglevel.level = Log.Level.ERROR
    elif verbose:
        STATE.loglevel.level = Log.Level.INFO
    elif debug:
        STATE.loglevel.level = Log.Level.DEBUG

    logger.debug(f"Python {PYTHON_VERSION} ({sys.executable})")
    logger.debug(f"Command: {sys.argv}")
    # Environment.get_executable()
    logger.debug(f"Working directory: {Path().resolve()}")
    logger.debug(f"Resources folder: {Environment.get_resources_folder()}")
    logger.debug(f"Data folder: {Environment.get_data_folder()}")
    logger.debug(f"Available languages: {sorted(AVAILABLE_LANGUAGES)} ({len(AVAILABLE_LANGUAGES)} entries)")
    logger.debug(f"Language (config / sys): ({CONFIG.language} / {get_system_locale()})")


__all__ = [
    "app_cmd",
]
