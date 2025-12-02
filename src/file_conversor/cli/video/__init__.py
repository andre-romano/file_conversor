
# src\file_conversor\cli\video\__init__.py


import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.video._typer import COMMAND_NAME

from file_conversor.cli.video.check_cmd import typer_cmd as check_cmd
from file_conversor.cli.video.compress_cmd import typer_cmd as compress_cmd
from file_conversor.cli.video.convert_cmd import typer_cmd as convert_cmd
from file_conversor.cli.video.enhance_cmd import typer_cmd as enhance_cmd
from file_conversor.cli.video.execute_cmd import typer_cmd as execute_cmd
from file_conversor.cli.video.info_cmd import typer_cmd as info_cmd
from file_conversor.cli.video.list_formats_cmd import typer_cmd as list_formats_cmd
from file_conversor.cli.video.mirror_cmd import typer_cmd as mirror_cmd
from file_conversor.cli.video.resize_cmd import typer_cmd as resize_cmd
from file_conversor.cli.video.rotate_cmd import typer_cmd as rotate_cmd

_ = get_translation()

video_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Video file manipulation (requires FFMpeg external library)"),
)

# TRANSFORMATION_PANEL
video_cmd.add_typer(convert_cmd)
video_cmd.add_typer(compress_cmd)
video_cmd.add_typer(enhance_cmd)
video_cmd.add_typer(mirror_cmd)
video_cmd.add_typer(rotate_cmd)
video_cmd.add_typer(resize_cmd)


# OTHERS_PANEL
video_cmd.add_typer(check_cmd)
video_cmd.add_typer(info_cmd)
video_cmd.add_typer(list_formats_cmd)
video_cmd.add_typer(execute_cmd)

__all__ = [
    "video_cmd",
]
