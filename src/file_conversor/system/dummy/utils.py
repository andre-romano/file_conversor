# src\file_conversor\system\dummy\utils.py

import os


def is_admin() -> bool:
    """True if app running with admin priviledges, False otherwise."""
    return False


def reload_user_path():
    """Reload user PATH in current process."""
    # dummy method
    pass


def set_window_icon(
    window_title: str,
    icon_path: str | os.PathLike,
    cx: int = 0,
    cy: int = 0,
):
    """
    Set the icon of a window given its title.
    Note: Setting window icons is not supported in this dummy implementation.
    """
    # dummy method
    pass


__all__ = [
    "is_admin",
    "reload_user_path",
    "set_window_icon",
]
