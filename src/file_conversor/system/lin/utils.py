# src\file_conversor\system\lin\utils.py

import os
import platform

# Import only on Linux to avoid ImportError on other OSes
# if platform.system() == "Linux":
#     pass  # dummy, do nothing
# else:
#     pass  # Placeholder so the name exists


def is_admin() -> bool:
    """True if app running with admin priviledges, False otherwise."""
    return os.geteuid() == 0  # type: ignore


def reload_user_path():
    """Reload user PATH in current process."""
    # dummy, not needed in Linux
    pass


def set_window_icon(
    window_title: str,
    icon_path: str | os.PathLike,
    cx: int = 0,
    cy: int = 0,
):
    """
    Set the icon of a window given its title.
    Note: Setting window icons is not natively supported on Linux.
    This function is a placeholder and does not perform any action.
    """
    # Linux does not support setting window icons in the same way as Windows.
    pass


__all__ = [
    "is_admin",
    "reload_user_path",
    "set_window_icon",
]
