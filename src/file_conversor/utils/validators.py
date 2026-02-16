# src\file_conversor\utils\validators.py

import os
import sys

from pathlib import Path
from typing import Any, Callable, Iterable

import typer

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
    import math
    return math.isclose(num1, num2, rel_tol=rel_tol, abs_tol=abs_tol)


def is_zero(num: int | float) -> bool:
    """
    Determines if a number is effectively zero within a small tolerance.

    :param num: The number to check.
    """
    return is_close(num, 0.0, rel_tol=1e-9, abs_tol=1e-9)


def prompt_retry_on_exception[T](
        text: str,
        type: Callable[[Any], T],
        default: T | None = None,
        hide_input: bool = False,
        confirmation_prompt: bool | str = False,
        show_choices: bool = True,
        show_default: bool = True,
        callback: Callable[[T], bool] | None = None,
        retries: int = int(sys.maxsize),
) -> T:
    """
    Prompts the user for input, retrying on exception.

    :param text: The prompt text.
    :param default: The default value.
    :param hide_input: Whether to hide the input (for passwords).
    :param confirmation_prompt: Whether to ask for confirmation.
    :param type: The type of the input.
    :param show_choices: Whether to show choices (for Enum types).
    :param show_default: Whether to show the default value.
    :param callback: A callback function to validate the input.
    :param retries: The number of retries 
    :param prompt_kwargs: Additional keyword arguments for typer.prompt.

    :raises typer.Abort: If the user aborts the input or retries are exhausted.
    :return: The user input, validated by the callback if provided.
    """
    for _ in range(retries):
        try:
            res = typer.confirm(
                text=text,
                default=default if isinstance(default, bool) else False,  # noqa: S3358
                show_default=show_default,
            ) if type == bool else (
                typer.prompt(
                    text=text,
                    default=default,
                    hide_input=hide_input,
                    confirmation_prompt=confirmation_prompt,
                    show_choices=show_choices,
                    show_default=show_default,
                )
            )
            if res is None:
                return res
            res = type(res)
            match callback(res) if callback else True:
                case False:
                    raise typer.BadParameter("Invalid input.")
                case _:
                    return res
        except (KeyboardInterrupt, typer.Abort, typer.Exit):
            raise
        except Exception as e:
            print(f"ERROR: {e}")
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
    except ValueError as e:
        raise exception from e

    if size_value < 0:
        raise exception
    return data


def check_path_exists(data: str | Path | None, exists: bool = True) -> Path | None:
    if not data:
        return None
    data = Path(os.path.expandvars(data))
    if exists and not data.exists():
        raise typer.BadParameter(f"{_("File")} '{data}' {_("not found")}")
    if not exists and data.exists():
        raise typer.BadParameter(f"{_("File")} '{data}' {_("exists")}")
    return data


def check_file_exists(data: str | Path | None) -> Path | None:
    data = check_path_exists(data)
    if data and not data.is_file():
        raise typer.BadParameter(f"{_("Path")} '{data}' {_("is not a file")}")
    return data


def check_dir_exists(data: str | Path | None, mkdir: bool = False) -> Path | None:
    if not data:
        return None
    data = Path(os.path.expandvars(data))
    if mkdir:
        data.mkdir(parents=True, exist_ok=True)
    check_path_exists(data)
    if not data.is_dir():
        raise typer.BadParameter(f"{_("Path")} '{data}' {_("is not a directory")}")
    return data


def check_is_bool_or_none(data: Any) -> bool | None:
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


def check_file_format(filename_or_list: Path | Iterable[Path] | None, file_formats: Iterable[str], exists: bool = False):
    """
    Checks if the provided format is supported.

    :param filename_or_list: Filename or iterable list
    :param file_formats: Supported file formats
    :param exists: Check if file exists. Default False (do not check).

    :raises typer.BadParameter: Unsupported format, or file not found.
    :raises TypeError: Invalid parameter type.
    """
    file_list: list[Path] = [filename_or_list] if isinstance(filename_or_list, Path) else list(filename_or_list or [])
    for path in file_list:
        file_format = path.suffix[1:]
        if file_formats and file_format not in file_formats:
            raise typer.BadParameter(f"\n{_('Unsupported format')} '{file_format}'. {_('Supported formats are')}: {', '.join([str(f) for f in file_formats])}.")
        if exists:
            check_file_exists(path)
    return filename_or_list


def check_valid_options(data: Any | None, valid_options: Iterable[Any]) -> Any | None:
    if not data:
        return data
    if data not in valid_options:
        raise typer.BadParameter(f"'{data}' {_('is invalid.  Valid options are')} {', '.join([str(v) for v in valid_options])}.")
    return data


__all__ = [
    "prompt_retry_on_exception",
    "check_file_size_format",
    "check_path_exists",
    "check_file_exists",
    "check_dir_exists",
    "check_is_bool_or_none",
    "check_positive_integer",
    "check_file_format",
    "check_valid_options",
]
