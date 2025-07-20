
# src\cli\config_cmd.py

import typer

from typing import Annotated

from rich import print
from rich.pretty import Pretty

# user-provided modules
from backend import FFmpegBackend

from config import get_translation
from config import Configuration, State

from utils import check_positive_integer, check_format

# app configuration
_ = get_translation()
CONFIG = Configuration.get_instance()
STATE = State.get_instance()

# create command
config_cmd = typer.Typer()


# config show
@config_cmd.command(help=f"""
    {_('Show the current configuration of the application')}.
""")
def show():
    print(f"{_('Configuration')}:", Pretty(CONFIG, expand_all=True))


# config set
@config_cmd.command(help=f"""
    {_('Configure the default options for the file converter.')}

    **{_('Example')}:** `file_conversor configure --video-bitrate 5000`
    **{_('Example')}:** `file_conversor configure --audio-bitrate 128`
""")
def set(
    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],
):
    # update the configuration dictionary
    CONFIG.update({
        "audio-bitrate": audio_bitrate,
        "video-bitrate": video_bitrate,
    })
    CONFIG.save()
    show()
    print(
        f"{_('Configuration file')} {_('updated')}.")
