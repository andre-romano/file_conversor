# src\file_conversor\utils\typer.py

import typer

from pathlib import Path
from typing import Annotated, Any, Iterable, List

# user-provided modules
from file_conversor.config.locale import get_translation
from file_conversor.utils.validators import check_file_exists, check_dir_exists, check_file_format, check_positive_integer, check_valid_options, check_video_resolution

_ = get_translation()


def InputFilesArgument(backend_or_iterable: type | dict | list | None = None):
    if not backend_or_iterable:
        return typer.Argument(
            help=f"{_('Input files')}",
            callback=lambda x: check_file_format(x, [], exists=True),
        )
    elif isinstance(backend_or_iterable, (dict, list)):
        list_formats: list[str] | dict[str, Any] = backend_or_iterable
    else:
        list_formats: list[str] | dict[str, Any] = backend_or_iterable.SUPPORTED_IN_FORMATS
    return typer.Argument(
        help=f"{_('Input files')} ({', '.join(list_formats)})",
        callback=lambda x: check_file_format(x, list_formats, exists=True),
    )


def FormatOption(backend_or_iterable: type | dict | list):
    """--format, -f"""
    if isinstance(backend_or_iterable, (dict, list)):
        list_formats: list[str] | dict[str, Any] = backend_or_iterable
    else:
        list_formats: list[str] | dict[str, Any] = backend_or_iterable.SUPPORTED_OUT_FORMATS
    return typer.Option(
        "--format", "-f",
        help=f"{_('Output format')} ({', '.join(list_formats)})",
        callback=lambda x: check_valid_options(x, list_formats),
    )


def OutputDirOption():
    """--output-dir, -od"""
    return typer.Option(
        "--output-dir", "-od",
        help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
        callback=lambda x: check_dir_exists(x, mkdir=True),
    )


def OutputFileOption(backend: type):
    """--output-file, -of"""
    return typer.Option(
        "--output-file", "-of",
        help=f"{_('Output file')} ({', '.join(backend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same 1st input file as output name')}).",
        callback=lambda x: check_file_format(x, backend.SUPPORTED_OUT_FORMATS),
    )

#################
# IMAGE OPTIONS #
#################


def QualityOption(prompt: bool | str = False):
    """--quality, -q"""
    return typer.Option(
        "--quality", "-q",
        help=_("Image quality. Valid values are between 1-100."),
        prompt=prompt,
        min=1, max=100,
    )


def AxisOption(prompt: bool | str = False):
    """--axis, -a"""
    return typer.Option(
        "--axis", "-a",
        help=_("Mirror axis. Valid values are 'x' (mirror horizontally) or 'y' (flip vertically)."),
        prompt=prompt,
        callback=lambda x: check_valid_options(x, valid_options=['x', 'y']),
    )


def DPIOption(prompt: bool | str = False):
    """--dpi, -d"""
    return typer.Option(
        "--dpi", "-d",
        help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
        prompt=prompt,
        min=40, max=3600,
    )


def BrightnessOption(prompt: bool | str = False):
    """--brightness, -b"""
    return typer.Option(
        "--brightness", "-b",
        prompt=prompt,
        help=_("Adjust brightness. brightness = 1.00 means no change. brightness < 1.00 makes image black. brightness > 1.00 makes image lighter."),
    )


def ContrastOption(prompt: bool | str = False):
    """--contrast, -ct"""
    return typer.Option(
        "--contrast", "-ct",
        prompt=prompt,
        help=_("Adjust contrast. contrast = 1.00 means no change. contrast < 1.00 reduces contrast (grayish image). contrast > 1.00 increases contrast."),
    )


def ColorOption(prompt: bool | str = False):
    """--color, -cl"""
    return typer.Option(
        "--color", "-cl",
        prompt=prompt,
        help=_("Adjust color. color = 1.00 means no change. color < 1.00 reduces color saturation. color > 1.00 increases color saturation."),
    )


def SharpnessOption(prompt: bool | str = False):
    """--sharpness, -s"""
    return typer.Option(
        "--sharpness", "-s",
        prompt=prompt,
        help=_("Adjust sharpness. sharpness = 1.00 means no change. sharpness < 1.00 makes image more blurry. sharpness > 1.00 increases image crispness (and noise as well)."),
    )


def RadiusOption(prompt: bool | str = False):
    """--radius, -r"""
    return typer.Option(
        "--radius", "-r",
        help=f'{_("Box radius (in pixels).")}',
        prompt=prompt,
        min=1,
    )

#################
# PDF OPTIONS   #
#################


def PasswordOption():
    """--password, -p"""
    return typer.Option(
        "--password", "-p",
        help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
    )

#################
# VIDEO OPTIONS #
#################


def AudioBitrateOption(prompt: bool | str = False):
    """--audio-bitrate, -ab"""
    return typer.Option(
        "--audio-bitrate", "-ab",
        help=f"{_("Audio bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
        prompt=prompt,
        callback=lambda x: check_positive_integer(x, allow_zero=True),
    )


def VideoBitrateOption(prompt: bool | str = False):
    """--video-bitrate, -vb"""
    return typer.Option(
        "--video-bitrate", "-vb",
        help=f"{_("Video bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
        prompt=prompt,
        callback=lambda x: check_positive_integer(x, allow_zero=True),
    )


def AudioCodecOption(available_options: Iterable[str], prompt: bool | str = False):
    """--audio-codec, -ac"""
    return typer.Option(
        "--audio-codec", "-ac",
        help=f'{_("Audio codec. Not all codecs are supported in a given format container (run `file_conversor video list-formats` for more information). Available options are:")} {", ".join(available_options)}. {_('Defaults to None (use the default for the file container)')}.',
        prompt=prompt,
        callback=lambda x: check_valid_options(x, available_options),
    )


def VideoCodecOption(available_options: Iterable[str], prompt: bool | str = False):
    """--video-codec, -vc"""
    return typer.Option(
        "--video-codec", "-vc",
        help=f'{_("Video codec. Not all codecs are supported in a given format container (run `file_conversor video list-formats` for more information). Available options are:")} {", ".join(available_options)}. {_('Defaults to None (use the default for the file container)')}.',
        prompt=prompt,
        callback=lambda x: check_valid_options(x, available_options),
    )


def SpeedPresetOption(available_options: Iterable[str], prompt: bool | str = False):
    """--speed-preset, -sp"""
    return typer.Option(
        "--speed-preset", "-sp",
        help=f'{_("Video codec speed preset. Slower speed = Higher quality. Available options are:")} {", ".join(available_options)}. {_('Defaults to None (use the default for the file container)')}.',
        prompt=prompt,
        callback=lambda x: check_valid_options(x, available_options),
    )


def ResolutionOption(prompt: bool | str = False):
    """--resolution, -rs"""
    return typer.Option(
        "--resolution", "-rs",
        help=f'{_("Video target resolution. Format WIDTH:HEIGHT (in pixels). Defaults to None (use same resolution as video source)")}',
        prompt=prompt,
        callback=check_video_resolution,
    )


def FPSOption(prompt: bool | str = False):
    """--fps, -fp"""
    return typer.Option(
        "--fps", "-fp",
        help=f'{_("Target video FPS (frames per second). Uses ``minterpolate`` filter to adjust fps. Defaults to None (use same fps as video source)")}',
        prompt=prompt,
        min=1,
    )


def VideoRotationOption(prompt: bool | str = False):
    """--rotation, -r"""
    return typer.Option(
        "--rotation", "-r",
        help=f'{_("Rotate video (clockwise). Available options are:")} {", ".join(['-180', '-90', '90', '180'])}. Defaults to None (do not rotate).',
        prompt=prompt,
        callback=lambda x: check_valid_options(x, [-180, -90, 90, 180]),
    )


def GammaOption(prompt: bool | str = False):
    """--gamma, -g"""
    return typer.Option(
        "--gamma", "-g",
        prompt=prompt,
        help=f'{_("Adjust gamma")}. {_('gamma = 1.00 means no change. gamma < 1.00 makes image more darker. gamma > 1.00 increases image lightenss')}.',
    )


def UnsharpOption():
    """--unsharp, -u"""
    return typer.Option(
        "--unsharp", "-u",
        help=f'{_("Increase video sharpness (using unsharp mask). May increase image noise.")}. {_('Defaults to False (do not apply filter)')}.',
        is_flag=True,
    )


def DeshakeOption():
    """--deshake, -d"""
    return typer.Option(
        "--deshake", "-d",
        help=f'{_("Deshake video (attempt to fix vertical/horizontal span from handrecoding)")}. {_('Defaults to False (do not apply filter)')}.',
        is_flag=True,
    )
