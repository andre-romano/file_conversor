# src\platform\mac\__init__.py

import platform

# Import only on Darwin to avoid ImportError on other OSes
if platform.system() == "Darwin":
    # do nothing
    pass
else:
    pass  # Placeholder so the name exists


def reload_user_path():
    """Reload user PATH in current process."""
    # dummy method (not needed in mac)
    pass
