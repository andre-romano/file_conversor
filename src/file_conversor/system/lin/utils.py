# src\file_conversor\system\lin\utils.py

import os
import platform

# Import only on Linux to avoid ImportError on other OSes
if platform.system() == "Linux":
    pass  # dummy, do nothing
else:
    pass  # Placeholder so the name exists


def is_admin() -> bool:
    """True if app running with admin priviledges, False otherwise."""
    return os.geteuid() == 0  # type: ignore


def reload_user_path():
    """Reload user PATH in current process."""
    # dummy, not needed in Linux
    pass
