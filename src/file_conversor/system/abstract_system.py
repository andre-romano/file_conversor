# src/file_conversor\system\abstract_system.py

import platform

from enum import Enum
from typing import Protocol

# user-provided imports
from file_conversor.config import Log

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class SystemProtocol(Protocol):
    @classmethod
    def is_admin(cls) -> bool:
        """True if app running with admin priviledges, False otherwise."""
        ...

    @classmethod
    def reload_user_path(cls):
        """Reload user PATH in current process."""
        ...


class AbstractSystem(SystemProtocol):
    class Platform(Enum):
        MACOS = "Darwin"
        LINUX = "Linux"
        WINDOWS = "Windows"

        @classmethod
        def get(cls) -> 'AbstractSystem.Platform':
            try:
                return cls(platform.system())
            except ValueError:
                logger.warning(f"Unknown platform: {platform.system()}")
                raise NotImplementedError(f"Platform {platform.system()} is not supported.")

        def __str__(self) -> str:
            return f"{self.get_name()} {self.get_version()} ({self.get_arch()})"

        def get_name(self):
            return self.value

        def get_version(self):
            return platform.version()

        def get_arch(self):
            return platform.machine()


__all__ = [
    "AbstractSystem",
]
