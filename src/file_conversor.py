
# src/file_conversor.py

import typer

from rich import print

from typing import Annotated

# user-provided imports
from cli import config_cmd, audio_video_cmd, pdf_cmd

from config import get_translation
from config import Configuration, State

# Get app config
_ = get_translation()
CONFIG = Configuration.get_instance()
STATE = State.get_instance()

# Create a Typer CLI application
app_cmd = typer.Typer(
    rich_markup_mode="markdown",
    no_args_is_help=True,
)

# PANELS
CONFIG_PANEL = _("Utils and Config")
MULTIMEDIA_PANEL = _("Multimedia files")

# REGISTER SUBCOMMANDS
app_cmd.add_typer(audio_video_cmd,
                  name="audio_video",
                  help=_("Audio / Video file manipulation"),
                  rich_help_panel=MULTIMEDIA_PANEL)

app_cmd.add_typer(pdf_cmd,
                  name="pdf",
                  help=_("PDF file manipulation"),
                  rich_help_panel=MULTIMEDIA_PANEL)

app_cmd.add_typer(config_cmd,
                  name="config",
                  help=_("Configure default options"),
                  rich_help_panel=CONFIG_PANEL)

# confirmacoes
# typer.confirm(f"Deletar {arquivo}?"):


# help
@app_cmd.command(
    help=f"""
    {_('Show the application help')}
    """,
    rich_help_panel=CONFIG_PANEL)
def help():
    ctx = typer.Context(typer.main.get_command(app_cmd))
    print(ctx.command.get_help(ctx))


# Main callback, to process global options
@app_cmd.callback(
    help=f"""
        # File Conversor - CLI

        **{_('Features')}:**

        - {_('Compress image / audio / video / doc / spreadsheet files')}

        - {_('Convert image / audio / video / doc / spreadsheet files')}

        - {_('Configure default options for conversion / compression')}

        - {_('Supports various input and output formats')} (mp3, mp4, jpg, png, pdf, docx, xlsx, csv, etc)
    """,
    epilog=f"""
        {_('For more information, visit')} [http://www.github.com/andre-romano/file_conversor](http://www.github.com/andre-romano/file_conversor)
    """)
def main_callback(
        verbose: Annotated[bool, typer.Option(
            "--verbose", "-v",
            help=_("Enable verbose output"),
            is_flag=True,
        )] = False,
):
    if verbose:
        print(f"{_('Verbose output')}: [blue][bold]{_('ENABLED')}[/bold][/blue]")
        STATE["verbose"] = True


# Entry point of the app
def main():
    app_cmd()


# Start the application
if __name__ == "__main__":
    main()
