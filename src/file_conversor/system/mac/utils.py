# src\file_conversor\system\mac\utils.py

import os
import platform

# Import only on Darwin to avoid ImportError on other OSes
if platform.system() == "Darwin":
    # do nothing
    pass
else:
    pass  # Placeholder so the name exists


def is_admin() -> bool:
    """True if app running with admin priviledges, False otherwise."""
    return os.geteuid() == 0  # type: ignore


def reload_user_path():
    """Reload user PATH in current process."""
    # dummy method (not needed in mac)
    pass
