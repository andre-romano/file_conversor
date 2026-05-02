# src/file_conversor/dependency/apt_pkg_manager.py

import shutil

from pathlib import Path
from typing import override

from file_conversor.config.locale import get_translation
from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager
from file_conversor.system import AbstractSystem, System


_ = get_translation()


class AptPackageManager(AbstractPackageManager):
    """Package manager for Debian / Ubuntu / Mint (apt)."""

    def __init__(
        self,
        dependencies: dict[str, str],
        env: list[str | Path] | None = None,
    ) -> None:
        super().__init__(dependencies=dependencies, env=env)

    @override
    def _get_pkg_manager_installed(self) -> str | None:
        return shutil.which("apt-get")

    @override
    def _get_supported_oses(self) -> set[AbstractSystem.Platform]:
        return {System.Platform.LINUX}

    @override
    def get_missing_dependencies(self) -> set[str]:
        # Skip entirely if apt-get is not available on this system
        if not self._get_pkg_manager_installed():
            return set()
        return super().get_missing_dependencies()

    @override
    def _get_cmd_install_pkg_manager(self) -> list[str]:
        raise RuntimeError("apt-get is a system package manager and cannot be installed by this tool.")

    @override
    def _post_install_pkg_manager(self) -> None:
        pass

    @override
    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["sudo", "apt-get", "install", "-y", dependency]


__all__ = [
    "AptPackageManager",
]
