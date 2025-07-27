
# src/file_conversor.py

import os
import platform

from cli.app_cmd import app_cmd

# Import winreg only on Windows to avoid ImportError on other OSes
system = platform.system()
if system == "Windows":
    import winreg
else:
    winreg = None  # Placeholder so the name exists


def reload_user_path_win():
    """Reload user PATH in current process."""
    if winreg is None:
        return
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
        user_path, _ = winreg.QueryValueEx(key, "PATH")
        os.environ["PATH"] = user_path + os.pathsep + os.environ["PATH"]


# Entry point of the app
def main():
    if system == "Windows":
        reload_user_path_win()
    app_cmd()


# Start the application
if __name__ == "__main__":
    main()
