# src\file_conversor\system\__init__.py

"""Stores platform specific methods"""

import platform

PLATFORM_WINDOWS = "Windows"
PLATFORM_LINUX = "Linux"
PLATFORM_MACOS = "Darwin"
PLATFORM_UNKNOWN = ""

CURR_PLATFORM = platform.system()

# dynamically load modules, as needed
if CURR_PLATFORM == PLATFORM_WINDOWS:
    # WINDOWS OS
    from file_conversor.system.win import reload_user_path, is_admin

elif CURR_PLATFORM == PLATFORM_LINUX:
    # LINUX OS
    from file_conversor.system.lin import reload_user_path, is_admin

elif CURR_PLATFORM == PLATFORM_MACOS:
    # MACOS OS
    from file_conversor.system.mac import reload_user_path, is_admin

else:
    # UNKNOWN OS
    CURR_PLATFORM = PLATFORM_UNKNOWN
    from file_conversor.system.dummy import reload_user_path, is_admin
