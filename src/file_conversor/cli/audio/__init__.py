
# src\file_conversor\cli\audio\__init__.py


import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.audio._typer import COMMAND_NAME

from file_conversor.cli.audio.check_cmd import typer_cmd as check_cmd
from file_conversor.cli.audio.convert_cmd import typer_cmd as convert_cmd
from file_conversor.cli.audio.info_cmd import typer_cmd as info_cmd

_ = get_translation()

audio_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Audio file manipulation (requires FFMpeg external library)"),
)

# CONVERSION_PANEL
audio_cmd.add_typer(convert_cmd)
audio_cmd.add_typer(info_cmd)
audio_cmd.add_typer(check_cmd)

__all__ = [
    "audio_cmd",
]
