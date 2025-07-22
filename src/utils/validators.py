# src/utils/validators.py

import os
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
        raise typer.BadParameter(f"\nUnsupported format '{format}'. Supported formats are: {', '.join(format_dict)}.")
    return format


def check_pdf_ext(filepath: str | None) -> str | None:
    if not filepath:
        return filepath
    ext = os.path.splitext(filepath)[1].lower()
    if ext != ".pdf":
        raise ValueError(f"File '{filepath}' is not a PDF file!")
    return filepath


def check_pdf_exists(filepath: str):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist!")
    return filepath
