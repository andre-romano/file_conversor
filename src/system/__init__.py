# src\platform\__init__.py

"""Stores platform specific methods"""

import platform

PLATFORM = platform.system()

# dynamically load modules, as needed
if PLATFORM == "Windows":
    from system.win import reload_user_path
elif PLATFORM == "Linux":
    from system.lin import reload_user_path
elif PLATFORM == "Darwin":
    from system.mac import reload_user_path
else:
    from system.dummy import reload_user_path
