# src\platform\lin.py

import platform

# Import only on Linux to avoid ImportError on other OSes
if platform.system() == "Linux":
    pass  # dummy, do nothing
else:
    pass  # Placeholder so the name exists


def reload_user_path():
    """Reload user PATH in current process."""
    # dummy, not needed in Linux
    pass
