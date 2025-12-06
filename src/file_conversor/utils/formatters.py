# src\file_conversor\utils\formatters.py

import json
import math
import re
import traceback
import typer

from pathlib import Path
from typing import Any, Iterable, Sequence

# user-provided modules
from file_conversor.config import State, get_translation

from file_conversor.utils.command_manager import CommandManager

STATE = State.get_instance()
_ = get_translation()


def escape_xml(text: Any | str | None) -> str:
    """
    Escape invalid characters for XML.
    """
    if text is None:
        return ""
    text = str(text)
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )


def parse_traceback_list(exc: Exception) -> list[str]:
    """
    Parse traceback to get specific frame.

    :param exc: Exception object.

    :return: List of str.
    """
    return traceback.format_exc().splitlines()


def parse_js_to_py(value: str) -> Any:
    # Attempt to convert to appropriate type
    # Handle null value
    if value is None or value.lower() in ('', 'null', 'none', 'undefined'):
        return None
    # Handle boolean values
    elif value.lower() in ('true', 'on'):
        return True
    elif value.lower() in ('false', 'off'):
        return False
    # Handle numeric values
    elif re.match(r'^-?\d+([\.,]\d+)?$', value):
        if '.' in value or ',' in value:
            return float(value.replace(',', '.'))
        else:
            return int(value)
    # Handle JSON arrays and objects
    elif value[0] in ('[', '{',) and value[-1] in (']', '}',):
        return json.loads(value.replace("'", '"'))
    return value  # return as string


def parse_ffmpeg_filter(filter: str | None) -> tuple[str, list, dict]:
    """
    Parse FFmpeg filter string to name, args, kwargs.

    :param filter: FFmpeg filter string.
    :returns: (name, args, kwargs)
    """
    if not filter:
        return "", [], {}
    splitted = filter.split("=", maxsplit=1)
    name = splitted[0]
    args = splitted[1].split(":") if len(splitted) > 1 else []
    kwargs = {}
    for arg in args.copy():
        arg_splitted = arg.split("=")
        arg_name = arg_splitted[0]
        arg_data = arg_splitted[1] if len(arg_splitted) > 1 else ""
        if not arg_data:
            continue
        kwargs[arg_name] = arg_data
        args.remove(arg)
    return name, args, kwargs


def parse_image_resize_scale(scale: float | None, width: int | None, quiet: bool):
    if not scale and not width:
        if quiet:
            raise RuntimeError(f"{_('Scale and width not provided')}")
        userinput = str(typer.prompt(f"{_('Output image scale (e.g., 1.5)')}"))
        scale = float(userinput)
    return scale


def parse_pdf_rotation(rotation: list[str], last_page: int) -> dict[int, int]:
    """Parse PDF rotation argument to dict of page: degree (0-based)."""
    # get rotation dict in format {page: rotation}
    rotation_dict = {}
    for arg in rotation:
        match = re.search(r'(\d+)(-(\d*))?:(-?\d+)', arg)
        if not match:
            raise RuntimeError(f"{_('Invalid rotation instruction')} '{arg}'. {_("Valid format is 'begin-end:degree' or 'page:degree'")}.")

        # check user input
        begin = int(match.group(1)) - 1
        end = begin
        if match.group(3):
            end = int(match.group(3)) - 1
        elif match.group(2):
            end = last_page - 1
        degree = int(match.group(4))
        if end < begin:
            raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

        # create rotation_dict
        for page_num in range(begin, end + 1):
            rotation_dict[page_num] = degree
    return rotation_dict


def parse_pdf_pages(pages: list[str] | str | None) -> list[int]:
    """Parse PDF pages argument to list of page numbers (0-based)."""
    if not pages:
        pages_str = typer.prompt(f"{_('Pages to extract [comma-separated list] (e.g., 1-3, 7-7)')}")
        pages = str(pages_str)

    if isinstance(pages, str):
        pages = [p.strip() for p in pages.split(",")]

    # parse user input
    pages_list: list[int] = []
    for arg in pages:
        match = re.compile(r'(\d+)(-(\d*))?').search(arg)
        if not match:
            raise RuntimeError(f"{_('Invalid page instruction')} '{arg}'. {_("Valid format is 'page' or 'begin-end'")}.")

        # check user input
        begin = int(match.group(1)) - 1
        end = int(match.group(3)) - 1 if match.group(3) else begin

        if end < begin:
            raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

        # create pages list
        pages_list.extend(range(begin, end + 1))
    return pages_list


def normalize_degree(deg: float | int) -> int:
    """Normalize clockwise degree to 0-360"""
    # parse rotation argument
    degree = int(math.fmod(deg, 360))
    if degree < 0:
        degree += 360  # fix rotation signal
    return degree


def parse_bytes(target_size: str | None) -> int:
    """
    Parse file size string (e.g., 100.5M, 2G) to bytes. 

    :return: Size in bytes.
    """
    if not target_size or target_size == "0":
        return 0
    size_unit = target_size[-1].upper()
    size_value = float(target_size[:-1])
    if size_unit.isdigit():
        return round(float(target_size))
    elif size_unit == "K":
        return round(size_value * 1024.0)
    elif size_unit == "M":
        return round(size_value * 1024.0 * 1024.0)
    elif size_unit == "G":
        return round(size_value * 1024.0 * 1024.0 * 1024.0)
    elif size_unit == "T":
        return round(size_value * 1024.0 * 1024.0 * 1024.0 * 1024.0)
    raise ValueError(f"{_('Invalid size format')} '{target_size}'.")


def format_bytes(size: float | int) -> str:
    """Format size in bytes, KB, MB, GB, or TB"""
    # Size in bytes to a human-readable string
    size = float(size)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def format_bitrate(bps: int) -> str:
    """Format bitrate in bps, kbps, Mbps, Gbps, Tbps etc."""
    if bps >= 1024 * 1024 * 1024 * 1024:
        return f"{bps / (1024 * 1024 * 1024 * 1024):.1f} Tbps"
    if bps >= 1024 * 1024 * 1024:
        return f"{bps / (1024 * 1024 * 1024):.1f} Gbps"
    if bps >= 1024 * 1024:
        return f"{bps / (1024 * 1024):.1f} Mbps"
    elif bps >= 1024:
        return f"{bps / 1024:.1f} Kbps"
    return f"{bps} bps"


def format_alphanumeric(text: str) -> str:
    """Format text to be alphanumeric only (remove non-alphanumeric characters)."""
    formatted = text
    formatted = re.sub(r'[áàâäãå]', 'a', formatted)
    formatted = re.sub(r'[éèëê]', 'e', formatted)
    formatted = re.sub(r'[íïìî]', 'i', formatted)
    formatted = re.sub(r'[óòöôõ]', 'o', formatted)
    formatted = re.sub(r'[úüùû]', 'u', formatted)
    formatted = re.sub(r'[çc]', 'c', formatted)
    formatted = re.sub(r'[ñn]', 'n', formatted)
    formatted = re.sub(r'[\s]+', ' ', formatted)
    formatted = re.sub(r'[^a-zA-Z0-9_ ]', '', formatted)
    return formatted.strip()


def format_file_types_webview(*file_types: str, description: str = "") -> str:
    """
    Format file types for PyWebView file dialogs.

    :param file_types: File type patterns (e.g., '*.png', '*.jpg').
    :param description: Description for the file types (e.g., 'Image Files').

    :return: Formatted file types string for PyWebView.
    """
    if not file_types:
        return f'{format_alphanumeric(_("All Files"))} (*.*)'
    if not description:
        description = _("Custom Files")
    parsed_types = [ft if ft.startswith("*.") else f"*.{ft.lstrip('.')}" for ft in file_types]
    return f'{format_alphanumeric(description)} ({";".join(parsed_types)})'


def format_py_to_js(value: Any) -> str:
    """Convert Python value to JavaScript-compatible string."""
    if isinstance(value, Path):
        value = str(value.resolve())
    data = json.dumps(value)
    if data[0] in ('"', "'") and data[-1] in ('"', "'"):
        # Strip quotes and wrap in backticks
        return f"`{data[1:-1]}`"
    return data


def format_traceback_str(exc: Exception, debug: bool = True) -> str:
    """
    Format exception traceback as string.

    :param exc: Exception object.
    :param debug: bool: Whether to include detailed traceback information.

    :return: Formatted traceback string.
    """
    exc_formatted = f'[bold red]{type(exc).__name__}[/]: {str(exc)}'
    if not debug:
        return exc_formatted

    stack_str_list = parse_traceback_list(exc)
    return '\n'.join(stack_str_list[:-1] + [exc_formatted])


def format_traceback_html(exc: Exception, debug: bool = True) -> str:
    """
    Format exception traceback as HTML.

    :param exc: Exception object.
    :param debug: bool: Whether to include detailed traceback information.

    :return: Formatted traceback HTML.
    """
    tab = "&nbsp;&nbsp;"
    exc_formatted = f'<b style="color:red;">{type(exc).__name__}</b>: {str(exc)}'
    if not debug:
        return exc_formatted

    stack_str_list = parse_traceback_list(exc)
    return '<br>'.join([
        escape_xml(s).replace(' ', "&nbsp;").replace('\t', tab).replace('\n', '<br>')
        for s in stack_str_list[:-1]
    ] + [exc_formatted])


def format_in_out_files_tuple(
    input_files: list[Path],
    format: str,
    output_dir: Path,
):
    """
    Get input and output files for conversion.

    :param input_files: List of input file paths.
    :param format: Output file format.
    :param output_dir: Output directory path.

    :raises FileExistsError: if output file exists and overwrite is disabled.
    """
    files = [
        (input_file, output_dir / CommandManager.get_output_file(input_file, suffix=f".{format.lstrip('.')}"))
        for input_file in input_files
    ]
    for input_file, output_file in files:
        if not STATE["overwrite-output"] and output_file.exists():
            raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")
    return files


__all__ = [
    "escape_xml",
    "parse_traceback_list",
    "parse_js_to_py",
    "parse_ffmpeg_filter",
    "parse_image_resize_scale",
    "parse_pdf_rotation",
    "parse_pdf_pages",
    "normalize_degree",
    "parse_bytes",
    "format_bytes",
    "format_bitrate",
    "format_alphanumeric",
    "format_file_types_webview",
    "format_py_to_js",
    "format_traceback_str",
    "format_traceback_html",
    "format_in_out_files_tuple",
]
