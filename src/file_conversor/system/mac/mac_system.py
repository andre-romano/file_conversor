# src\file_conversor\system\mac\mac_system.py

import os

from typing import override

# user-provided imports
from file_conversor.system.abstract_system import AbstractSystem


class MacSystem(AbstractSystem):
    """MacOS specific system utilities."""
    @classmethod
    @override
    def is_admin(cls) -> bool:
        """True if app running with admin priviledges, False otherwise."""
        return os.geteuid() == 0  # type: ignore

    @classmethod
    @override
    def reload_user_path(cls):
        """Reload user PATH in current process."""
        # dummy method (not needed in mac)


__all__ = [
    "MacSystem",
]
