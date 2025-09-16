# src\file_conversor\utils\formatters.py

import math
import re
import typer


# user-provided modules
from file_conversor.config.locale import get_translation

_ = get_translation()


def parse_ffmpeg_filter(filter: str | None) -> tuple[str, list, dict]:
    """return (name, args, kwargs)"""
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
    # get rotation dict in format {page: rotation}
    rotation_dict = {}
    for arg in rotation:
        match = re.search(r'(\d+)(-(\d*)){0,1}:([-]{0,1}\d+)', arg)
        if not match:
            raise RuntimeError(f"{_('Invalid rotation instruction')} '{arg}'. {_("Valid format is 'begin-end:degree' or 'page:degree'")}.")

        # check user input
        begin = int(match.group(1)) - 1
        end = begin
        if match.group(3):
            end = int(match.group(3)) - 1
        elif match.group(2):
            end = last_page
        degree = int(match.group(4))
        if end < begin:
            raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

        # create rotation_dict
        for page_num in range(begin, end + 1):
            rotation_dict[page_num] = degree
    return rotation_dict


def parse_pdf_pages(pages: list[str] | None) -> list[int]:
    if not pages:
        pages_str = typer.prompt(f"{_('Pages to extract [comma-separated list] (e.g., 1-3, 7-7)')}")
        pages = [p.strip() for p in str(pages_str).split(",")]

    # parse user input
    pages_list: list[int] = []
    for arg in pages:
        match = re.compile(r'(\d+)-(\d*){0,1}').search(arg)
        if not match:
            raise RuntimeError(f"{_('Invalid page instruction')} '{arg}'. {_("Valid format is 'begin-end'")}.")

        # check user input
        begin = int(match.group(1)) - 1
        end = int(match.group(2)) - 1

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
    if size_unit == "K":
        return round(size_value * 1024.0)
    elif size_unit == "M":
        return round(size_value * 1024.0 * 1024.0)
    elif size_unit == "G":
        return round(size_value * 1024.0 * 1024.0 * 1024.0)
    return round(size_value)


def format_bytes(size: float) -> str:
    """Format size in bytes, KB, MB, GB, or TB"""
    # Size in bytes to a human-readable string
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def format_bitrate(bps: int) -> str:
    """Format bitrate in bps, kbps or Mbps"""
    if bps >= 1_000_000:
        return f"{bps / 1_000_000:.2f} Mbps"
    elif bps >= 1000:
        return f"{bps / 1000:.0f} kbps"
    return f"{bps} bps"
