# src/file_conversor\system\abstract_system.py


from abc import abstractmethod
from enum import Enum
from typing import override

# user-provided imports
from file_conversor.config import LOG


logger = LOG.getLogger(__name__)


class AbstractSystem:
    class Platform(Enum):
        MACOS = "Darwin"
        LINUX = "Linux"
        WINDOWS = "Windows"

        @classmethod
        def get(cls) -> 'AbstractSystem.Platform':
            import platform
            try:
                return cls(platform.system())
            except ValueError as e:
                logger.warning(f"Unknown platform: {platform.system()}")
                raise RuntimeError(f"Platform {platform.system()} is not supported.") from e

        @override
        def __str__(self) -> str:
            return f"{self.get_name()} {self.get_version()} ({self.get_arch()})"

        def get_name(self):
            return self.value

        def get_version(self):
            import platform
            return platform.version()

        def get_arch(self):
            import platform
            return platform.machine()

        def get_processor(self):
            import platform
            return platform.processor()

    @classmethod
    @abstractmethod
    def is_admin(cls) -> bool:
        """True if app running with admin priviledges, False otherwise."""

    @classmethod
    @abstractmethod
    def reload_user_path(cls):
        """Reload user PATH in current process."""


__all__ = [
    "AbstractSystem",
]
