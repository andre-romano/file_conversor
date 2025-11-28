
# src\file_conversor\system\win\utils.py

import os
import platform
import subprocess
import time

from pathlib import Path

# Import winreg only on Windows to avoid ImportError on other OSes
if platform.system() == "Windows":
    import winreg
    import ctypes
else:
    # Placeholder so the names exists
    winreg = None
    ctypes = None


def _get_window_hwnd(window_title: str) -> int:
    """
    Get the window handle (HWND) for a given window title.

    :param window_title: The title of the window.
    :return: The HWND of the window.
    :raises RuntimeError: If the window is not found or ctypes is unavailable.
    """
    if ctypes is None:
        raise RuntimeError(f"ctypes is not available on this platform ({platform.system()}).")

    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd == 0:
        raise RuntimeError(f"user32.FindWindowW: Window with title '{window_title}' not found.")
    return hwnd


def is_admin() -> bool:
    """True if app running with admin priviledges, False otherwise."""
    try:
        if ctypes:
            res = ctypes.windll.shell32.IsUserAnAdmin()  # pyright: ignore[reportAttributeAccessIssue]
            if isinstance(res, int):
                return res != 0
            if isinstance(res, bool):
                return res
    except:
        pass
    return False


def reload_user_path():
    """Reload user PATH in current process."""
    if winreg is None:
        return
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:  # pyright: ignore[reportAttributeAccessIssue]
        user_path, _ = winreg.QueryValueEx(key, "PATH")  # pyright: ignore[reportAttributeAccessIssue]
        os.environ["PATH"] = user_path + os.pathsep + os.environ["PATH"]


def restart_explorer():
    # Step 1: kill explorer.exe
    subprocess.run(
        ["taskkill", "/f", "/im", "explorer.exe"],
        capture_output=True,
        text=True,  # Capture output as text (Python 3.7+)
        check=True,
    )
    # Wait briefly to ensure process termination
    time.sleep(0.5)  # Increased delay for stability
    # Step 2: Restart explorer.exe
    subprocess.Popen(
        "explorer.exe",
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,  # Detach from Typer
    )


def set_window_icon(
    window_title: str,
    icon_path: str | Path,
    cx: int = 0,
    cy: int = 0,
):
    """
    Set the icon of a window given its title.

    :param window_title: The title of the window.
    :param icon_path: Path to the icon file.
    :param cx: Width position of the icon.
    :param cy: Height position of the icon.

    :raises RuntimeError: If an error occurs while setting the window icon.
    """
    if ctypes is None:
        raise RuntimeError(f"ctypes is not available on this platform ({platform.system()}).")

    hwnd = _get_window_hwnd(window_title)

    hicon = ctypes.windll.user32.LoadImageW(
        0,  # hInstance
        str(icon_path),  # icon_path
        1,  # IMAGE_ICON
        cx,  # cx
        cy,  # cy
        0x00000010,  # LR_LOADFROMFILE
    )
    if hicon == 0:
        raise RuntimeError(f"user32.LoadImageW: Failed to load icon from '{icon_path}'.")

    ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, hicon)  # WM_SETICON (small)
    ctypes.windll.user32.SendMessageW(hwnd, 0x80, 1, hicon)  # WM_SETICON (big)


__all__ = [
    "is_admin",
    "reload_user_path",
    "restart_explorer",
    "set_window_icon",
]
