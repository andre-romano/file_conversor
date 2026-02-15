# src\file_conversor\system\lin\utils.py

import os

from typing import override

from file_conversor.system.abstract_system import AbstractSystem


class LinuxSystem(AbstractSystem):
    @classmethod
    @override
    def is_admin(cls) -> bool:
        """True if app running with admin priviledges, False otherwise."""
        return os.geteuid() == 0  # type: ignore

    @classmethod
    @override
    def reload_user_path(cls):
        """Reload user PATH in current process."""
        # dummy, not needed in Linux


__all__ = [
    "LinuxSystem",
]
