
# src\file_conversor\cli\audio_video\__init__.py


import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.audio_video._typer import COMMAND_NAME

from file_conversor.cli.audio_video.check_cmd import typer_cmd as check_cmd
from file_conversor.cli.audio_video.execute_cmd import typer_cmd as execute_cmd
from file_conversor.cli.audio_video.enhance_cmd import typer_cmd as enhance_cmd
from file_conversor.cli.audio_video.info_cmd import typer_cmd as info_cmd
from file_conversor.cli.audio_video.mirror_cmd import typer_cmd as mirror_cmd
from file_conversor.cli.audio_video.resize_cmd import typer_cmd as resize_cmd
from file_conversor.cli.audio_video.rotate_cmd import typer_cmd as rotate_cmd
from file_conversor.cli.audio_video.to_avi_cmd import typer_cmd as to_avi_cmd

_ = get_translation()

audio_video_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Audio / Video file manipulation (requires FFMpeg external library)"),
)

# TRANSFORMATION_PANEL
audio_video_cmd.add_typer(enhance_cmd)
audio_video_cmd.add_typer(mirror_cmd)
audio_video_cmd.add_typer(rotate_cmd)
audio_video_cmd.add_typer(resize_cmd)

# CONVERSION_PANEL
audio_video_cmd.add_typer(to_avi_cmd)

# OTHERS_PANEL
audio_video_cmd.add_typer(info_cmd)
audio_video_cmd.add_typer(check_cmd)
audio_video_cmd.add_typer(execute_cmd)
