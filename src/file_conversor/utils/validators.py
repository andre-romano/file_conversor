# src\file_conversor\utils\validators.py

import subprocess
import typer

from pathlib import Path
from typing import Any, Iterable, List

# user provided imports
from file_conversor.config.locale import get_translation

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
        raise typer.BadParameter(_("Must be a positive integer."))
    return bitrate


def check_file_format(filename_or_iter: list | dict | set | str | Path | None, format_dict: dict | list, exists: bool = False):
    """
    Checks if the provided format is supported.

    :param filename_or_iter: Filename or iterable list
    :param format_dict: Format {format:options} or [format]
    :param exists: Check if file exists. Default False (do not check).

    :raises typer.BadParameter: Unsupported format, or file not found.
    :raises TypeError: Invalid parameter type.
    """
    file_list = []
    if isinstance(filename_or_iter, (list, dict, set)):
        file_list = list(filename_or_iter)
    elif isinstance(filename_or_iter, (str | Path)):
        file_list.append(str(filename_or_iter))
    elif filename_or_iter is None:
        return filename_or_iter
    else:
        raise TypeError(f"{_('Invalid type')} '{type(filename_or_iter)}' {_('for')} filename_or_iter. {_('Valid values are Iterable | str | None')}.")
    for filename in file_list:
        file_path = Path(filename)
        file_format = file_path.suffix[1:].lower()
        if file_format not in format_dict:
            raise typer.BadParameter(f"\n{_('Unsupported format')} '{file_format}'. {_('Supported formats are')}: {', '.join(format_dict)}.")
        if exists and not file_path.exists() and not file_path.is_file():
            raise typer.BadParameter(f"{_("File")} '{filename}' {_("not found")}")
    return filename_or_iter


def check_valid_options(data: Any | None, valid_options: Iterable):
    if data not in valid_options:
        raise typer.BadParameter(f"'{data}' is invalid.  Valid options are {', '.join(valid_options)}.")
    return data
