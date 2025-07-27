# src/utils/validators.py

import os
import typer

from config.locale import get_translation

_ = get_translation()


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


def check_format(format: str, format_dict: dict | list):
    """
    Checks if the provided format is supported.
    """
    if format not in format_dict:
        raise typer.BadParameter(f"\n{_('Unsupported format')} '{format}'. {_('Supported formats are')}: {', '.join(format_dict)}.")
    return format


def check_pdf_ext(filepath: str | None) -> str | None:
    if not filepath:
        return filepath
    ext = os.path.splitext(filepath)[1].lower()
    if ext != ".pdf":
        raise ValueError(f"{_('File')} '{filepath}' {_('is not a PDF file')}!")
    return filepath


def check_pdf_exists(filepath: str):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"{_('File')} '{filepath}' {_('does not exist')}!")
    return filepath
