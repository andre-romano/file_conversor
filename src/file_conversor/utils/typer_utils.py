# src\file_conversor\utils\typer.py

import typer

from pathlib import Path
from typing import Annotated, List

# user-provided modules
from file_conversor.config.locale import get_translation
from file_conversor.utils.validators import check_file_exists, check_dir_exists, check_file_format, check_valid_options

_ = get_translation()


def InputFilesArgument(backend: type | None = None):
    if not backend:
        return typer.Argument(
            help=f"{_('Input files')}",
            callback=lambda x: check_file_format(x, [], exists=True),
        )
    return typer.Argument(
        help=f"{_('Input files')} ({', '.join(backend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, backend.SUPPORTED_IN_FORMATS, exists=True),
    )


def FormatOption(backend: type):
    """--format, -f"""
    return typer.Option(
        "--format", "-f",
        help=f"{_('Output format')} ({', '.join(backend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: check_valid_options(x, backend.SUPPORTED_OUT_FORMATS),
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


def QualityOption():
    """--quality, -q"""
    return typer.Option(
        "--quality", "-q",
        help=_("Image quality. Valid values are between 1-100."),
        min=1, max=100,
    )


def AxisOption():
    """--axis, -a"""
    return typer.Option(
        "--axis", "-a",
        help=_("Mirror axis. Valid values are 'x' (mirror horizontally) or 'y' (flip vertically)."),
        callback=lambda x: check_valid_options(x, valid_options=['x', 'y']),
    )


def DPIOption():
    """--dpi, -d"""
    return typer.Option(
        "--dpi", "-d",
        help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
        min=40, max=3600,
    )


def PasswordOption():
    """--password, -p"""
    return typer.Option(
        "--password", "-p",
        help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
    )
