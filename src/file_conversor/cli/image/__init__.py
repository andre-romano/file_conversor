# src\file_conversor\cli\image\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.image._typer import COMMAND_NAME

from file_conversor.cli.image.antialias_cmd import typer_cmd as antialias_cmd
from file_conversor.cli.image.blur_cmd import typer_cmd as blur_cmd
from file_conversor.cli.image.compress_cmd import typer_cmd as compress_cmd
from file_conversor.cli.image.convert_cmd import typer_cmd as convert_cmd
from file_conversor.cli.image.enhance_cmd import typer_cmd as enhance_cmd
from file_conversor.cli.image.filter_cmd import typer_cmd as filter_cmd
from file_conversor.cli.image.info_cmd import typer_cmd as info_cmd
from file_conversor.cli.image.mirror_cmd import typer_cmd as mirror_cmd
from file_conversor.cli.image.render_cmd import typer_cmd as render_cmd
from file_conversor.cli.image.resize_cmd import typer_cmd as resize_cmd
from file_conversor.cli.image.rotate_cmd import typer_cmd as rotate_cmd
from file_conversor.cli.image.to_pdf_cmd import typer_cmd as to_pdf_cmd
from file_conversor.cli.image.unsharp_cmd import typer_cmd as unsharp_cmd

_ = get_translation()

image_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Image file manipulation"),
)
# CONVERSION_PANEL
image_cmd.add_typer(convert_cmd)
image_cmd.add_typer(render_cmd)
image_cmd.add_typer(to_pdf_cmd)

# TRANSFORMATION_PANEL
image_cmd.add_typer(compress_cmd)
image_cmd.add_typer(mirror_cmd)
image_cmd.add_typer(rotate_cmd)
image_cmd.add_typer(resize_cmd)

# FILTER_PANEL
image_cmd.add_typer(antialias_cmd)
image_cmd.add_typer(blur_cmd)
image_cmd.add_typer(enhance_cmd)
image_cmd.add_typer(filter_cmd)
image_cmd.add_typer(unsharp_cmd)

# OTHERS_PANEL
image_cmd.add_typer(info_cmd)

__all__ = [
    "image_cmd",
]
