# src\file_conversor\system\__init__.py

"""Stores platform specific methods"""

import platform
from rich import print

_PLATFORM_WINDOWS = "Windows"
_PLATFORM_LINUX = "Linux"
_PLATFORM_MACOS = "Darwin"
_PLATFORM_UNKNOWN = ""

_CURR_PLATFORM = platform.system()


def is_windows():
    return _CURR_PLATFORM == _PLATFORM_WINDOWS


def is_linux():
    return _CURR_PLATFORM == _PLATFORM_LINUX


def is_macos():
    return _CURR_PLATFORM == _PLATFORM_MACOS


def is_unknown():
    return _CURR_PLATFORM == _PLATFORM_UNKNOWN


# dynamically load modules, as needed
if _CURR_PLATFORM == _PLATFORM_WINDOWS:
    # WINDOWS OS
    from file_conversor.system.win import *
    print("[bold blue]System detected[/]: Windows.")

elif _CURR_PLATFORM == _PLATFORM_LINUX:
    # LINUX OS
    from file_conversor.system.lin import *
    print("[bold blue]System detected[/]: Linux.")

elif _CURR_PLATFORM == _PLATFORM_MACOS:
    # MACOS OS
    from file_conversor.system.mac import *
    print("[bold blue]System detected[/]: macOS.")

else:
    # UNKNOWN OS
    _CURR_PLATFORM = _PLATFORM_UNKNOWN
    from file_conversor.system.dummy import *
    print("[bold blue]System detected[/]: Unknown OS.")
