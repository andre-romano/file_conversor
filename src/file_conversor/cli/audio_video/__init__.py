
# src\file_conversor\cli\audio_video\__init__.py


import typer

# user-provided modules
from file_conversor.cli.audio_video.convert_cmd import typer_cmd as convert_cmd
from file_conversor.cli.audio_video.info_cmd import typer_cmd as info_cmd

audio_video_cmd = typer.Typer()
audio_video_cmd.add_typer(info_cmd)
audio_video_cmd.add_typer(convert_cmd)
