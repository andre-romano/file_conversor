# src\file_conversor\cli\utils\utils_typer.py

from typing import Iterable

import typer

from typer.models import OptionInfo

# user-provided modules
from file_conversor.config.locale import get_translation
from file_conversor.utils.validators import (
    check_dir_exists,
    check_file_format,
    check_file_size_format,
    check_video_resolution,
)


_ = get_translation()


def InputFilesArgument(file_formats: Iterable[str] | None = None):
    file_formats = list(file_formats or [])
    if not file_formats:
        file_formats = ["*"]
    return typer.Argument(
        help=f"{_('Input files')} ({', '.join(file_formats)})",
        callback=lambda x: check_file_format(x, [] if "*" in file_formats else file_formats, exists=True),  # pyright: ignore[reportUnknownArgumentType]
    )


def FormatOption() -> OptionInfo:
    """--format, -f"""
    return typer.Option(
        "--format", "-f",
        help=f"{_('Output format')}",
    )


def OutputDirOption() -> OptionInfo:
    """--output-dir, -od"""
    return typer.Option(
        "--output-dir", "-od",
        help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
        callback=lambda x: check_dir_exists(x, mkdir=True),  # pyright: ignore[reportUnknownArgumentType]
    )


def OutputFileOption(file_formats: Iterable[str]) -> OptionInfo:
    """--output-file, -of"""
    file_formats = list(file_formats)
    return typer.Option(
        "--output-file", "-of",
        help=f"{_('Output file')} ({', '.join(file_formats)}). {_('Defaults to None')} ({_('use the same 1st input file as output name')}).",
        callback=lambda x: check_file_format(x, file_formats),  # pyright: ignore[reportUnknownArgumentType]
    )

#################
# IMAGE OPTIONS #
#################


def QualityOption(prompt: bool | str = False) -> OptionInfo:
    """--quality, -q"""
    return typer.Option(
        "--quality", "-q",
        help=_("Image quality. Valid values are between 1-100."),
        prompt=prompt,
        min=1, max=100,
    )


def AxisOption() -> OptionInfo:
    """--axis, -a"""
    return typer.Option(
        "--axis", "-a",
        help=f"{_('Mirror axis (horizontal, vertical)')}.",
    )


def DPIOption(prompt: bool | str = False) -> OptionInfo:
    """--dpi, -d"""
    return typer.Option(
        "--dpi", "-d",
        help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
        prompt=prompt,
        min=40, max=3600,
    )


def BrightnessOption(prompt: bool | str = False) -> OptionInfo:
    """--brightness, -b"""
    return typer.Option(
        "--brightness", "-b",
        prompt=prompt,
        help=_("Adjust brightness. brightness = 1.00 means no change. brightness < 1.00 makes image black. brightness > 1.00 makes image lighter."),
        min=0.0,
    )


def ContrastOption(prompt: bool | str = False) -> OptionInfo:
    """--contrast, -ct"""
    return typer.Option(
        "--contrast", "-ct",
        prompt=prompt,
        help=_("Adjust contrast. contrast = 1.00 means no change. contrast < 1.00 reduces contrast (grayish image). contrast > 1.00 increases contrast."),
        min=0.0,
    )


def ColorOption(prompt: bool | str = False) -> OptionInfo:
    """--color, -cl"""
    return typer.Option(
        "--color", "-cl",
        prompt=prompt,
        help=_("Adjust color. color = 1.00 means no change. color < 1.00 reduces color saturation. color > 1.00 increases color saturation."),
        min=0.0,
    )


def SharpnessOption(prompt: bool | str = False) -> OptionInfo:
    """--sharpness, -s"""
    return typer.Option(
        "--sharpness", "-s",
        prompt=prompt,
        help=_("Adjust sharpness. sharpness = 1.00 means no change. sharpness < 1.00 makes image more blurry. sharpness > 1.00 increases image crispness (and noise as well)."),
        min=0.0,
    )


def GammaOption(prompt: bool | str = False) -> OptionInfo:
    """--gamma, -g"""
    return typer.Option(
        "--gamma", "-g",
        prompt=prompt,
        help=f'{_("Adjust gamma")}. {_('gamma = 1.00 means no change. gamma < 1.00 makes image more darker. gamma > 1.00 increases image lightenss')}.',
        min=0.0,
    )


def RadiusOption(prompt: bool | str = False) -> OptionInfo:
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


def PasswordOption() -> OptionInfo:
    """--password, -p"""
    return typer.Option(
        "--password", "-p",
        help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
    )

#################
# VIDEO OPTIONS #
#################


def TargetFileSizeOption(prompt: bool | str = False) -> OptionInfo:
    """--target-size, -ts"""
    return typer.Option(
        "--target-size", "-ts",
        help=f"{_("Target file size.")} {_('Format "size[K|M|G]". If 0, do not limit output file size (use encoding speed and quality options to calculate output file size).')}",
        prompt=prompt,
        callback=check_file_size_format,  # pyright: ignore[reportUnknownArgumentType]
    )


def AudioBitrateOption(prompt: bool | str = False) -> OptionInfo:
    """--audio-bitrate, -ab"""
    return typer.Option(
        "--audio-bitrate", "-ab",
        help=f"{_("Audio bitrate in kbps.")} {_('If -1, let FFmpeg decide best bitrate.')}",
        prompt=prompt,
        min=1,
    )


def VideoBitrateOption(prompt: bool | str = False) -> OptionInfo:
    """--video-bitrate, -vb"""
    return typer.Option(
        "--video-bitrate", "-vb",
        help=f"{_("Video bitrate in kbps.")} {_('Overrides video quality setting (if set). If -1, use video quality setting to encode video using variable bitrate (CRF) encoding (if supported by codec, otherwise use default bitrate for codec/container)')}.",
        prompt=prompt,
        min=1,
    )


def AudioCodecOption(prompt: bool | str = False) -> OptionInfo:
    """--audio-codec, -ac"""
    return typer.Option(
        "--audio-codec", "-ac",
        help=f'{_("Audio codec. Not all codecs are supported in a given format container (run `file_conversor video list-formats` for more information).")} {_('Defaults to "default" (use the default for the file container)')}.',
        prompt=prompt,
    )


def VideoCodecOption(prompt: bool | str = False) -> OptionInfo:
    """--video-codec, -vc"""
    return typer.Option(
        "--video-codec", "-vc",
        help=f'{_("Video codec. Not all codecs are supported in a given format container (run `file_conversor video list-formats` for more information).")} {_('Defaults to "default" (use the default for the file container)')}.',
        prompt=prompt,
    )


def VideoProfileOption(prompt: bool | str = False) -> OptionInfo:
    """--video-profile, -vp"""
    return typer.Option(
        "--video-profile", "-vp",
        help=f'{_("Video profile.")} {_("Higher profiles result in higher compression, but require more decoding processing power")}.',
        prompt=prompt,
    )


def VideoEncodingSpeedOption(prompt: bool | str = False) -> OptionInfo:
    """--video-encoding-speed, -ves"""
    return typer.Option(
        "--video-encoding-speed", "-ves",
        help=f'{_("Video encoding speed/quality trade-off.")} {_("Faster encoding speed usually results in lower video quality and larger file size")}.',
        prompt=prompt,
    )


def VideoQualityOption(prompt: bool | str = False) -> OptionInfo:
    """--video-quality, -vq"""
    return typer.Option(
        "--video-quality", "-vq",
        help=f'{_("Video quality preset.")} {_("Higher quality usually results in larger file size. Video bitrate (if set) overrides this setting.")}.',
        prompt=prompt,
    )


def ResolutionOption(prompt: bool | str = False) -> OptionInfo:
    """--resolution, -rs"""
    return typer.Option(
        "--resolution", "-rs",
        help=f'{_("Video target resolution. Format WIDTH:HEIGHT (in pixels). Defaults to 0:0 (use same resolution as video source)")}',
        prompt=prompt,
        callback=check_video_resolution,
    )


def FPSOption(prompt: bool | str = False) -> OptionInfo:
    """--fps, -fp"""
    return typer.Option(
        "--fps", "-fp",
        help=f'{_("Target video FPS (frames per second). Uses ``minterpolate`` filter to adjust fps. Defaults to None (use same fps as video source)")}',
        prompt=prompt,
        min=1,
    )


def VideoRotationOption(prompt: bool | str = False) -> OptionInfo:
    """--rotation, -r"""
    return typer.Option(
        "--rotation", "-r",
        help=f'{_("Rotate video (clockwise).")} Defaults to None (do not rotate).',
        prompt=prompt,
    )


def UnsharpOption() -> OptionInfo:
    """--unsharp, -u"""
    return typer.Option(
        "--unsharp", "-u",
        help=f'{_("Increase video sharpness (using unsharp mask). May increase image noise.")}. {_('Defaults to False (do not apply filter)')}.',
        is_flag=True,
    )


def DeshakeOption() -> OptionInfo:
    """--deshake, -d"""
    return typer.Option(
        "--deshake", "-d",
        help=f'{_("Deshake video (attempt to fix vertical/horizontal span from handrecoding)")}. {_('Defaults to False (do not apply filter)')}.',
        is_flag=True,
    )


__all__ = [
    "InputFilesArgument",
    "FormatOption",
    "OutputDirOption",
    "OutputFileOption",
    "QualityOption",
    "AxisOption",
    "DPIOption",
    "BrightnessOption",
    "ContrastOption",
    "ColorOption",
    "SharpnessOption",
    "RadiusOption",
    "PasswordOption",
    "TargetFileSizeOption",
    "AudioBitrateOption",
    "VideoBitrateOption",
    "AudioCodecOption",
    "VideoCodecOption",
    "VideoEncodingSpeedOption",
    "VideoQualityOption",
    "ResolutionOption",
    "FPSOption",
    "VideoRotationOption",
    "GammaOption",
    "UnsharpOption",
    "DeshakeOption",
]
