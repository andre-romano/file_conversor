# src/file_conversor\system\abstract_system.py


from enum import Enum
from typing import Protocol, override

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
            import platform
            try:
                return cls(platform.system())
            except ValueError as e:
                logger.warning(f"Unknown platform: {platform.system()}")
                raise NotImplementedError(f"Platform {platform.system()} is not supported.") from e

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


__all__ = [
    "AbstractSystem",
]
