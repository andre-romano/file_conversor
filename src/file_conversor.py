
# src/file_conversor.py

import json
import locale
import subprocess
import time
import typer
import gettext  # app translations / locales

from rich import print
from rich.pretty import Pretty
from rich.progress import Progress, SpinnerColumn, TextColumn

from pathlib import Path
from typing import Annotated, Optional

# user-provided imports
from backend import FFmpegBackend
from utils.file import File
from utils.validators import check_positive_integer, check_format

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

# Get translations
lang, encoding = locale.getlocale()
translation = gettext.translation(
    'messages', 'locales',
    languages=[lang if lang else "en_US", "en_US"],
    fallback=False
)
_ = translation.gettext

# Create a Typer CLI application
app_cmd = typer.Typer(
    rich_markup_mode="markdown",
    no_args_is_help=True,
)

# panels
CONFIG_PANEL = _("Utils and Config")
MULTIMEDIA_PANEL = _("Multimedia files")

# subcommands
audio_video_cmd = typer.Typer()
config_cmd = typer.Typer()

# register subcommands
app_cmd.add_typer(audio_video_cmd, name="audio_video",
                  help=_("Audio / Video manipulation commands"),
                  rich_help_panel=MULTIMEDIA_PANEL)
app_cmd.add_typer(config_cmd, name="config",
                  help=_("Configure default options"),
                  rich_help_panel=CONFIG_PANEL)

# confirmacoes
# typer.confirm(f"Deletar {arquivo}?"):


@app_cmd.command()
def info(name: Annotated[str, typer.Option("--name", "-n", prompt=True)]):
    """Sauda uma pessoa pelo nome"""
    typer.echo(f"Olá, {name}!")

    typer.secho("Texto em vermelho", fg=typer.colors.RED)
    typer.secho("Texto em verde negrito", fg=typer.colors.GREEN, bold=True)
    typer.secho("Fundo azul", bg=typer.colors.BLUE)

    with Progress(SpinnerColumn(), TextColumn("{task.description} [progress.description]"), transient=True,) as progress:
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


# audio_video convert
@audio_video_cmd.command(name="convert",
                         epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor audio_video convert input_file.webm output_file.mp4 --audio-bitrate 192`

    - `file_conversor audio_video convert input_file.mp4 output_file.mp3`
    """)
def audio_video_convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file path')} ({', '.join(FFmpegBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: x if check_format(
            File(x).get_extension(), FFmpegBackend.SUPPORTED_IN_FORMATS
        ) else x,
    )],
    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file path')} ({', '.join(FFmpegBackend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: x if check_format(
            File(x).get_extension(), FFmpegBackend.SUPPORTED_OUT_FORMATS
        ) else x,
    )],
    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],
):
    f"""
    {_('Convert a audio/video file to a different format.')}

    {_('This command can be used to convert audio or video files to the specified format.')}
    """
    process: subprocess.Popen | None = None
    in_options = []
    out_options = []

    # configure out options
    out_options.extend(["-b:a", f"{audio_bitrate}k"])
    if File(output_file).get_extension() in FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS:
        out_options.extend(["-b:v", f"{video_bitrate}k"])

    # execute ffmpeg
    ffmpeg_backend = FFmpegBackend(
        input_file,
        output_file,
        verbose=STATE["verbose"],
        in_options=in_options,
        out_options=out_options,
    )
    process = ffmpeg_backend.execute()

    # display current progress
    with Progress() as progress:
        ffmpeg_task = progress.add_task(
            f"[blue]{_('Processing file')}...", total=100)
        while process.poll() is None:
            progress.update(
                ffmpeg_task, completed=ffmpeg_backend.get_progress())
            time.sleep(0.25)

    process.wait()
    progress.update(ffmpeg_task, completed=100)

    if process.returncode == 0:
        print(f"--------------------------------")
        print(
            f"{_('FFMpeg convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green] ({process.returncode})")
        print(f"--------------------------------")
    else:
        # print output
        if process.stderr:
            for line in process.stderr:
                print(line)
        if process.stdout:
            for line in process.stdout:
                print(line)
        print(f"\n--------------------------------")
        print(
            f"{_('FFMpeg convertion')}: [red][bold]{_('FAILED')}[/bold][/red] ({process.returncode if process else "?"})")
        print(f"--------------------------------")


# audio_video info
@audio_video_cmd.command(name="info",
                         epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor audio_video info filename.webm`

    - `file_conversor audio_video info other_filename.mp3`
    """)
def audio_video_info(
    filename: Annotated[str, typer.Argument(
        help="File path",
        callback=lambda x: x if check_format(
            File(x).get_extension(), FFmpegBackend.SUPPORTED_IN_FORMATS
        ) else x,
    )],
):
    f"""
    {_('Get information about a audio/video file.')}

    {_('This command retrieves metadata and other information about the audio / video file')}:

    - {_('Format')} (mp3, mp4, mov, etc)

    - {_('Duration')} (HH:MM:SS)

    - Bitrate

    - {_('Other properties')}
    """
    pass


# config show
@config_cmd.command(name="show")
def config_show():
    f"""
    {_('Show the current configuration of the application')}.
    """
    print(f"{_('Configuration')}:", Pretty(CONFIG, expand_all=True))


# config set
@config_cmd.command(name="set")
def config_set(
    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],

    video_format: Annotated[str, typer.Option("--video-format", "-vf",
                                              help=f"{_('Video output format')} ({', '.join(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)})",
                                              callback=lambda x: check_format(
                                                  x, FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS),
                                              )] = CONFIG["video-format"],

    audio_format: Annotated[str, typer.Option("--audio-format", "-af",
                                              help=f"{_('Audio output format')} ({', '.join(FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS)})",
                                              callback=lambda x: check_format(
                                                  x, FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS),
                                              )] = CONFIG["audio-format"],
):
    f"""
    {_('Configure the default options for the file converter.')}

    **{_('Example')}:** `file_conversor configure --video-format mp4 --video-bitrate 5000`
    """
    # update the configuration dictionary
    CONFIG.update({
        "audio-bitrate": audio_bitrate,
        "video-bitrate": video_bitrate,
        "video-format": video_format,
        "audio-format": audio_format,
    })
    print(f"{_('Configuration')}:", Pretty(CONFIG, expand_all=True))
    config_path.write_text(json.dumps(CONFIG))
    typer.echo(
        f"{_('Configuration file')} '{str(config_path)}' {_('updated')}.")


# help
@app_cmd.command(rich_help_panel=CONFIG_PANEL)
def help():
    f"""
    {_('Show the application help')}
    """
    ctx = typer.Context(typer.main.get_command(app_cmd))
    print(ctx.command.get_help(ctx))


@app_cmd.callback(epilog=f"{_('For more information, visit')} [http://www.github.com/andre-romano/file_conversor](http://www.github.com/andre-romano/file_conversor)")
def main_callback(verbose: Annotated[bool, typer.Option("--verbose", "-v",
                                                        help=_(
                                                            "Enable verbose output"),
                                                        is_flag=True,
                                                        )] = False):
    f"""
    # File Conversor - CLI

    **{_('Features')}:**

    - {_('Compress image / audio / video / doc / spreadsheet files')}

    - {_('Convert image / audio / video / doc / spreadsheet files')}

    - {_('Configure default options for conversion / compression')}

    - {_('Supports various input and output formats')} (mp3, mp4, jpg, png, pdf, docx, xlsx, csv, etc)
    """
    if verbose:
        print(
            f"{_('Verbose output')}: [blue][bold]{_('ENABLED')}[/bold][/blue]")
        STATE["verbose"] = True


def main():
    app_cmd()


# Start the application
if __name__ == "__main__":
    main()
