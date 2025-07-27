
# src\cli\config_cmd.py

import typer

from typing import Annotated

from rich import print
from rich.pretty import Pretty

# user-provided modules
from config import Configuration, State
from config.locale import get_translation

from utils.validators import check_is_bool_or_none, check_positive_integer

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

    install_deps: Annotated[str | None, typer.Option("--install-deps", "-id",
                                                     help=_("Install missing external dependencies action. 'True' for auto install. 'False' to not install missing dependencies. 'None' to ask user for action."),
                                                     callback=check_is_bool_or_none,
                                                     )] = CONFIG["install-deps"],
):
    # update the configuration dictionary
    CONFIG.update({
        "audio-bitrate": audio_bitrate,
        "video-bitrate": video_bitrate,
        "install-deps": None if install_deps == "None" or install_deps is None else bool(install_deps),
    })
    CONFIG.save()
    show()
    print(f"{_('Configuration file')} {_('updated')}.")
