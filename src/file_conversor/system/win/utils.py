
# src\file_conversor\system\win\utils.py

import os
import platform
import subprocess
import time

# Import winreg only on Windows to avoid ImportError on other OSes
if platform.system() == "Windows":
    import winreg
    import ctypes
else:
    # Placeholder so the names exists
    winreg = None
    ctypes = None


def is_admin() -> bool:
    """True if app running with admin priviledges, False otherwise."""
    try:
        if ctypes:
            return ctypes.windll.shell32.IsUserAnAdmin()  # pyright: ignore[reportAttributeAccessIssue]
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
