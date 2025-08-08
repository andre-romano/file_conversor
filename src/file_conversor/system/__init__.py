# src\file_conversor\system\__init__.py

"""Stores platform specific methods"""

import platform

PLATFORM_WINDOWS = "Windows"
PLATFORM_LINUX = "Linux"
PLATFORM_MACOS = "Darwin"
PLATFORM_UNKNOWN = ""

CURR_PLATFORM = PLATFORM_UNKNOWN

# dynamically load modules, as needed
if platform.system() == PLATFORM_WINDOWS:
    # WINDOWS OS
    CURR_PLATFORM = PLATFORM_WINDOWS
    from file_conversor.system.win import reload_user_path, is_admin

elif platform.system() == PLATFORM_LINUX:
    # LINUX OS
    CURR_PLATFORM = PLATFORM_LINUX
    from file_conversor.system.lin import reload_user_path, is_admin

elif platform.system() == PLATFORM_MACOS:
    # MACOS OS
    CURR_PLATFORM = PLATFORM_MACOS
    from file_conversor.system.mac import reload_user_path, is_admin

else:
    # UNKNOWN OS
    CURR_PLATFORM = PLATFORM_UNKNOWN
    from file_conversor.system.dummy import reload_user_path, is_admin
