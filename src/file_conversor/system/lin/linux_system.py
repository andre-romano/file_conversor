# src\file_conversor\system\lin\utils.py

import os
from pathlib import Path

# user-provided imports
from file_conversor.system.abstract_system import AbstractSystem


class LinuxSystem(AbstractSystem):
    @classmethod
    def is_admin(cls) -> bool:
        """True if app running with admin priviledges, False otherwise."""
        return os.geteuid() == 0  # type: ignore

    @classmethod
    def reload_user_path(cls):
        """Reload user PATH in current process."""
        # dummy, not needed in Linux
        pass


__all__ = [
    "LinuxSystem",
]
