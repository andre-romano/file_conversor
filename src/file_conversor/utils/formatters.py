# src\file_conversor\utils\formatters.py

def format_bytes(size: float) -> str:
    """Format size in bytes, KB, MB, GB, or TB"""
    # Tamanho em bytes para string legível
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
