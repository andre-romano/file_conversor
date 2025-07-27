# src/utils/validators.py

import os
import typer

# user provided imports
from config.locale import get_translation

from utils.file import File

_ = get_translation()


def check_axis(axis: str) -> str:
    """"Check if axis in ('x', 'y')"""
    axis = axis.lower()
    if axis in ('x', 'y'):
        return axis
    raise ValueError(f"{_('Invalid axis value')} '{axis}'. {_('Valid values are "x" or "y".')}")


def check_is_bool_or_none(data: str | bool | None) -> bool | None:
    """
    Checks if the provided input is a valid bool or None.
    """
    if data is None or isinstance(data, bool):
        return data
    if isinstance(data, str):
        if data.lower() == "true":
            return True
        if data.lower() == "false":
            return False
        if data.lower() == "none":
            return None
    raise typer.BadParameter(_("Must be a bool or None."))


def check_positive_integer(bitrate: int | float):
    """
    Checks if the provided number is a positive integer.
    """
    if bitrate <= 0:
        raise typer.BadParameter(_("Bitrate must be a positive integer."))
    return bitrate


def check_file_format(filename: str | None, format_dict: dict | list, exists: bool = False):
    """
    Checks if the provided format is supported.

    :param filename: Filename
    :param format_dict: Format {format:options} or [format]
    :param exists: Check if file exists. Default False (do not check).
    """
    if filename is None:
        return filename
    file = File(filename)
    file_format = file.get_extension().lower()
    if file_format not in format_dict:
        raise typer.BadParameter(f"\n{_('Unsupported format')} '{file_format}'. {_('Supported formats are')}: {', '.join(format_dict)}.")
    if exists and not file.is_file():
        raise typer.BadParameter(f"{_("File")} '{filename}' {_("not found")}")
    return filename


def check_pdf_encrypt_algorithm(algorithm: str | None):
    if algorithm not in (None, "RC4-40", "RC4-128", "AES-128", "AES-256-R5", "AES-256"):
        raise typer.BadParameter(f"Encryption algorithm '{algorithm}' is invalid.  Valid options are 'RC4-40', 'RC4-128', 'AES-128', 'AES-256-R5', or 'AES-256'.")
    return algorithm
