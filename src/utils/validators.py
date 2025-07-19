# src/utils/validators.py

import typer


def check_positive_integer(bitrate: int | float):
    """
    Checks if the provided number is a positive integer.
    """
    if bitrate <= 0:
        raise typer.BadParameter("Bitrate must be a positive integer.")
    return bitrate


def check_format(format: str, format_dict: dict | list):
    """
    Checks if the provided format is supported.
    """
    if format not in format_dict:
        raise typer.BadParameter(
            f"\nUnsupported format '{format}'. Supported formats are: {', '.join(format_dict)}.")
    return format
