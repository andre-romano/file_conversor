# src\cli\app_cmd.py

import typer

from rich import print

from typing import Annotated

# user-provided imports
from cli import audio_video_cmd
from cli import batch_cmd
from cli import config_cmd
from cli import image_cmd
from cli import pdf_cmd

from config import Configuration, State, Log
from config.locale import get_translation

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
)

# PANELS
UTILS_CONFIG_PANEL = _("Utils and Config")
MULTIMEDIA_PANEL = _("Multimedia files")

# REGISTER SUBCOMMANDS
app_cmd.add_typer(audio_video_cmd,
                  name="audio_video",
                  help=_("Audio / Video file manipulation (requires FFMpeg external library)"),
                  rich_help_panel=MULTIMEDIA_PANEL)

app_cmd.add_typer(image_cmd,
                  name="image",
                  help=_("Image file manipulation"),
                  rich_help_panel=MULTIMEDIA_PANEL)

app_cmd.add_typer(pdf_cmd,
                  name="pdf",
                  help=_("PDF file manipulation"),
                  rich_help_panel=MULTIMEDIA_PANEL)

app_cmd.add_typer(batch_cmd,
                  name="batch",
                  help=f"""Batch file processing (task automation)

{_('The batch processing pipeline works by monitoring an input folder, passing those files to the next pipeline stage, and processing them inside that stage. This process continues (output of the current stage is the input of the next stage), until those files reach the end of the pipeline.')}



{_('Example')}:

- {_('Input folder')} => {_('Stage 1')} => {_('Stage 2')} => ... => {_('Output Folder')}
""",
    rich_help_panel=UTILS_CONFIG_PANEL)

app_cmd.add_typer(config_cmd,
                  name="config",
                  help=_("Configure default options"),
                  rich_help_panel=UTILS_CONFIG_PANEL)


# help
@app_cmd.command(
    help=f"{_('Show the application help')}",
    rich_help_panel=UTILS_CONFIG_PANEL)
def help():
    ctx = typer.Context(typer.main.get_command(app_cmd))
    print(ctx.command.get_help(ctx))


# Main callback, to process global options
@app_cmd.callback(
    help=f"""
        # File Conversor - CLI

        **{_('Features')}:**

        - {_('Compress image / audio / video / pdf files')}

        - {_('Convert image / audio / video / pdf files')}

        - {_('Batch file processing, for task automation using scripts')}
        
        - {_('Supports various input and output formats')} (mp3, mp4, mkv, jpg, png, webp, pdf, etc)
        
        - {_('Configure default options for conversion / compression')}
        
        - {_('Installs external dependencies automatically')}
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
):
    STATE.update({
        "no-log": no_log,
        "no-progress": no_progress,
        "quiet": quiet,
        "verbose": verbose,
        "debug": debug,
    })

    if no_log:
        logger.info(f"{_('File logging')}: [blue red]{_('DISABLED')}[/]")
        LOG.set_dest_folder(None)

    if no_progress:
        logger.info(f"{_('Progress bars')}: [blue red]{_('DISABLED')}[/]")

    if quiet:
        logger.info(f"{_('Quiet mode')}: [blue bold]{_('ENABLED')}[/]")
        LOG.set_level(Log.LEVEL_ERROR)
    if verbose:
        logger.info(f"{_('Verbose mode')}: [blue bold]{_('ENABLED')}[/]")
        LOG.set_level(Log.LEVEL_INFO)
    if debug:
        logger.info(f"{_('Debug mode')}: [blue bold]{_('ENABLED')}[/]")
        LOG.set_level(Log.LEVEL_DEBUG)
