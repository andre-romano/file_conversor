# src\file_conversor\utils\validators.py

import math
import sys
import typer

from pathlib import Path
from typing import Any, Callable, Iterable, List

# user provided imports
from file_conversor.config.locale import get_translation

_ = get_translation()


def is_close(num1: int | float, num2: int | float, rel_tol: float = 1e-9, abs_tol: float = 1e-9) -> bool:
    """
    Determines if two numbers are close to each other within a specified tolerance.

    :param num1: First number.
    :param num2: Second number.
    :param rel_tol: Relative tolerance.
    :param abs_tol: Absolute tolerance.
    """
    return math.isclose(num1, num2, rel_tol=rel_tol, abs_tol=abs_tol)


def is_zero(num: int | float) -> bool:
    """
    Determines if a number is effectively zero within a small tolerance.

    :param num: The number to check.
    """
    return is_close(num, 0.0, rel_tol=1e-9, abs_tol=1e-9)


def prompt_retry_on_exception(
        text: str,
        default: Any | None = None,
        hide_input: bool = False,
        confirmation_prompt: bool | str = False,
        type: Any | None = None,
        show_choices: bool = True,
        show_default: bool = True,
        check_callback: Callable[[Any], Any] | None = None,
        retries: int | None = None,
        **prompt_kwargs,
) -> Any:
    """
    Prompts the user for input, retrying on exception.

    :param text: The prompt text.
    :param default: The default value.
    :param hide_input: Whether to hide the input (for passwords).
    :param confirmation_prompt: Whether to ask for confirmation.
    :param type: The type of the input.
    :param show_choices: Whether to show choices (for Enum types).
    :param show_default: Whether to show the default value.
    :param check_callback: A callback function to validate the input.
    :param retries: The number of retries (None for infinite).
    :param prompt_kwargs: Additional keyword arguments for typer.prompt.

    :raises typer.Abort: If the user aborts the input or retries are exhausted.
    :return: The user input, validated by the callback if provided.
    """
    for _ in range(retries or int(sys.maxsize)):
        try:
            if type == bool:
                res = typer.confirm(
                    text=text,
                    default=default if isinstance(default, bool) else False,
                    show_default=show_default,
                )
            else:
                res = typer.prompt(
                    text=text,
                    default=default,
                    hide_input=hide_input,
                    confirmation_prompt=confirmation_prompt,
                    type=type,
                    show_choices=show_choices,
                    show_default=show_default,
                    **prompt_kwargs,
                )
            return check_callback(res) if check_callback else res
        except:
            pass
    raise typer.Abort()


def check_file_size_format(data: str | None) -> str | None:
    exception = typer.BadParameter(f"{_('Invalid file size')} '{data}'. {_('Valid file size is <size>[K|M|G]')}.")
    if not data or data == "0":
        return data

    size_unit = data[-1].upper()
    if size_unit not in ["K", "M", "G"]:
        raise exception

    size_value = -1
    try:
        size_value = float(data[:-1])
    except ValueError:
        raise exception

    if size_value < 0:
        raise exception
    return data


def check_video_resolution(data: str | None) -> str | None:
    if not data:
        return data
    if ":" not in data:
        raise typer.BadParameter(f"{_('Invalid format for video resolution')} '{data}'. {_('Valid format is WIDTH:HEIGHT')}.")
    width_height = data.split(":")
    if len(width_height) != 2:
        raise typer.BadParameter(f"{_('Invalid format for video resolution')} '{data}'. {_('Valid format is WIDTH:HEIGHT')}.")
    return data


def check_path_exists(data: str | Path | None, exists: bool = True):
    if not data:
        return data
    path = Path(data)
    if exists and not path.exists():
        raise typer.BadParameter(f"{_("File")} '{path}' {_("not found")}")
    if not exists and path.exists():
        raise typer.BadParameter(f"{_("File")} '{path}' {_("exists")}")
    return data


def check_file_exists(data: str | Path | None):
    check_path_exists(data)
    if data and not Path(data).is_file():
        raise typer.BadParameter(f"{_("Path")} '{data}' {_("is not a file")}")
    return data


def check_dir_exists(data: str | Path | None, mkdir: bool = False):
    if data and mkdir:
        Path(data).mkdir(parents=True, exist_ok=True)
    check_path_exists(data)
    if data and not Path(data).is_dir():
        raise typer.BadParameter(f"{_("Path")} '{data}' {_("is not a directory")}")
    return data


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


def check_positive_integer(num: int | float | None, allow_zero: bool = False):
    """
    Checks if the provided number is a positive integer.
    """
    if num is None:
        return None
    if num < 0 or (not allow_zero and is_close(num, 0)):
        raise typer.BadParameter(_("Must be a positive integer."))
    return num


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
        file_format = file_path.suffix[1:]
        if format_dict and file_format not in format_dict:
            raise typer.BadParameter(f"\n{_('Unsupported format')} '{file_format}'. {_('Supported formats are')}: {', '.join([str(f) for f in format_dict])}.")
        if exists:
            check_file_exists(file_path)
    return filename_or_iter


def check_valid_options(data: Any | None, valid_options: Iterable):
    if not data:
        return data
    if data not in valid_options:
        raise typer.BadParameter(f"'{data}' {_('is invalid.  Valid options are')} {', '.join([str(v) for v in valid_options])}.")
    return data


def check_ip_format(data: str | None) -> str | None:
    exception = typer.BadParameter(f"'{data}' {_('is not a valid IP address')}.")
    if not data:
        return data
    parts = data.split(".")
    if len(parts) != 4:
        raise exception
    for part in parts:
        try:
            number = int(part)
            if number < 0 or number > 255:
                raise exception
        except ValueError:
            raise exception
    return data


__all__ = [
    "prompt_retry_on_exception",
    "check_file_size_format",
    "check_video_resolution",
    "check_path_exists",
    "check_file_exists",
    "check_dir_exists",
    "check_is_bool_or_none",
    "check_positive_integer",
    "check_file_format",
    "check_valid_options",
    "check_ip_format",
]
