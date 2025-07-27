# src\platform\win.py

import os
import platform

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
