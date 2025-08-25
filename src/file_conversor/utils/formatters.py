# src\file_conversor\utils\formatters.py

import math


def normalize_degree(deg: float | int) -> int:
    """Normalize clockwise degree to 0-360"""
    # parse rotation argument
    degree = int(math.fmod(deg, 360))
    if degree < 0:
        degree += 360  # fix rotation signal
    return degree


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
