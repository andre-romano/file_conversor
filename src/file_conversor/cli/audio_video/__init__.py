
# src\file_conversor\cli\audio_video\__init__.py


import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.audio_video._typer import COMMAND_NAME

from file_conversor.cli.audio_video.convert_cmd import typer_cmd as convert_cmd
from file_conversor.cli.audio_video.info_cmd import typer_cmd as info_cmd

_ = get_translation()

audio_video_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Audio / Video file manipulation (requires FFMpeg external library)"),
)
audio_video_cmd.add_typer(info_cmd)
audio_video_cmd.add_typer(convert_cmd)
