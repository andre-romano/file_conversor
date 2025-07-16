
# src/file_conversor.py

import json
import time
import typer

from rich import print
from rich.pretty import Pretty
from rich.progress import track, Progress, SpinnerColumn, TextColumn

from pathlib import Path
from typing import Annotated, Optional

# user-provided imports
from backend import FFmpegBackend

# Define a STATE dictionary to hold application STATE
STATE = {
    "verbose": False,
}

# Define configuration dictionary
CONFIG = {
    "audio-bitrate": 192,    # Default audio bitrate in kbps
    "video-bitrate": 10000,  # Default video bitrate in kbps
    "video-format":  "mp4",  # Default output video format
    "audio-format":  "mp3",  # Default output audio format
}

# Load JSON configuration file
config_path = Path(f".config.json")
if config_path.exists():
    CONFIG.update(json.loads(config_path.read_text()))

# Create a Typer CLI application
app = typer.Typer(
    rich_markup_mode="markdown",
    no_args_is_help=True,
)

# # subcommands
# configure_cmd = typer.Typer()
# app.add_typer(configure_cmd, name="configure",
#               help="Configure the application")

# confirmacoes
# typer.confirm(f"Deletar {arquivo}?"):


def check_bitrate(bitrate: int):
    """
    Checks if the provided bitrate is a positive integer.
    """
    if bitrate <= 0:
        raise typer.BadParameter("Bitrate must be a positive integer.")
    return bitrate


def check_format(format: str, format_dict: dict | list):
    """
    Checks if the provided format is supported.
    """
    if format not in format_dict:
        raise typer.BadParameter(
            f"\nUnsupported format '{format}'. Supported formats are: {', '.join(format_dict)}.")
    return format


@app.command(rich_help_panel="Utils and Config")
def set_config(
    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help="Audio bitrate in kbps",
                                               callback=check_bitrate,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help="Video bitrate in kbps",
                                               callback=check_bitrate,
                                               )] = CONFIG["video-bitrate"],

    video_format: Annotated[str, typer.Option("--video-format", "-vf",
                                              help=f"Video output format ({', '.join(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)})",
                                              callback=lambda x: check_format(
                                                  x, FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS),
                                              )] = CONFIG["video-format"],

    audio_format: Annotated[str, typer.Option("--audio-format", "-af",
                                              help=f"Audio output format ({', '.join(FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS)})",
                                              callback=lambda x: check_format(
                                                  x, FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS),
                                              )] = CONFIG["audio-format"],
):
    """
    Configure the default options for the file converter.

    **Example:** `file_conversor configure --video-format mp4 --video-bitrate 5000`
    """
    # update the configuration dictionary
    CONFIG.update({
        "audio-bitrate": audio_bitrate,
        "video-bitrate": video_bitrate,
        "video-format": video_format,
        "audio-format": audio_format,
    })
    print(f"Configuration:", Pretty(CONFIG, expand_all=True))
    config_path.write_text(json.dumps(CONFIG))
    typer.echo(f"Configuration file '{str(config_path)}' updated.")


@app.command(rich_help_panel="Utils and Config")
def show_config():
    """
    Show the current configuration of the application.
    """
    print(f"Configuration:", Pretty(CONFIG, expand_all=True))


@app.command(rich_help_panel="Utils and Config")
def help():
    """
    Show the help message for the application.
    """
    ctx = typer.Context(typer.main.get_command(app))
    print(ctx.command.get_help(ctx))


@app.command()
def info(name: Annotated[str, typer.Option("--name", "-n", prompt=True)]):
    """Sauda uma pessoa pelo nome"""
    typer.echo(f"Olá, {name}!")

    typer.secho("Texto em vermelho", fg=typer.colors.RED)
    typer.secho("Texto em verde negrito", fg=typer.colors.GREEN, bold=True)
    typer.secho("Fundo azul", bg=typer.colors.BLUE)

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description} [progress.description]"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        time.sleep(3)

    with Progress() as progress:
        task1 = progress.add_task("[red]Downloading...", total=1000)
        task2 = progress.add_task("[green]Processing...", total=1000)
        # task3 = progress.add_task("[cyan]Cooking...", start=False, total=None)
        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            time.sleep(0.02)


@app.callback(epilog="For more information, visit [http://www.github.com/andre-romano/file_conversor](http://www.github.com/andre-romano/file_conversor)")
def main_callback(verbose: Annotated[bool, typer.Option("--verbose", "-v",
                                                        help="Enable verbose output",
                                                        is_flag=True,
                                                        )] = False):
    """
    # File Conversor - CLI

    **Features:**

    - Compress image / audio / video / doc / spreadsheet files

    - Convert image / audio / video / doc / spreadsheet files

    - Configure default options for conversion / compression

    - Supports various input and output formats
    """
    if verbose:
        print("Will write verbose output")
        STATE["verbose"] = True


def main():
    """
    Main function to run the Typer application.
    """
    app()


# Start the application
if __name__ == "__main__":
    main()
