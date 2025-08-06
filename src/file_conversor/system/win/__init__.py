# src\platform\win\__init__.py

import os
import platform
import subprocess
import time

# exports
from file_conversor.system.win.ctx_menu import WinContextMenu, WinContextCommand
from file_conversor.system.win.reg import WinRegFile, WinRegKey

# Import winreg only on Windows to avoid ImportError on other OSes
if platform.system() == "Windows":
    import winreg
else:
    winreg = None  # Placeholder so the name exists


def reload_user_path():
    """Reload user PATH in current process."""
    if winreg is None:
        return
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
        user_path, _ = winreg.QueryValueEx(key, "PATH")
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
