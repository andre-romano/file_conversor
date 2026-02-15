
# src\file_conversor\system\win\utils.py

import os

from pathlib import Path
from typing import override

# user-provided imports
from file_conversor.system.abstract_system import AbstractSystem


class WindowsSystem(AbstractSystem):
    @classmethod
    def _get_window_hwnd(cls, window_title: str) -> int:
        """
        Get the window handle (HWND) for a given window title.

        :param window_title: The title of the window.
        :return: The HWND of the window.

        :raises RuntimeError: If the window is not found or ctypes is unavailable.
        """
        import ctypes

        hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
        if hwnd == 0:
            raise RuntimeError(f"user32.FindWindowW: Window with title '{window_title}' not found.")
        return hwnd

    @classmethod
    @override
    def is_admin(cls) -> bool:
        import ctypes
        try:
            res = ctypes.windll.shell32.IsUserAnAdmin()  # pyright: ignore[reportAttributeAccessIssue]
            if isinstance(res, int):
                return res != 0
            if isinstance(res, bool):
                return res
        except Exception:
            """In case of any exception (e.g., ctypes not available), assume not admin."""
        return False

    @classmethod
    @override
    def reload_user_path(cls):
        """Reload user PATH in current process."""
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:  # pyright: ignore[reportAttributeAccessIssue]
            user_path, _ = winreg.QueryValueEx(key, "PATH")  # pyright: ignore[reportAttributeAccessIssue]
            os.environ["PATH"] = user_path + os.pathsep + os.environ["PATH"]

    @classmethod
    def restart_explorer(cls):
        import subprocess
        import time

        # Step 1: kill explorer.exe
        subprocess.run(
            ["taskkill", "/f", "/im", "explorer.exe"],  # noqa: S607
            capture_output=True,
            text=True,  # Capture output as text (Python 3.7+)
            check=True,
        )
        # Wait briefly to ensure process termination
        time.sleep(0.5)  # Increased delay for stability
        # Step 2: Restart explorer.exe
        subprocess.Popen(  # noqa: S602
            "explorer.exe",  # noqa: S607
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,  # Detach from Typer
        )

    @classmethod
    def set_window_icon(
        cls,
        window_title: str,
        icon_path: str | Path,
        cx: int = 0,
        cy: int = 0,
    ):
        import ctypes
        hwnd = cls._get_window_hwnd(window_title)

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
    "WindowsSystem",
]
