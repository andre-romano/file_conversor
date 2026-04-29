# src/file_conversor/dependency/dnf_pkg_manager.py

import shutil

from pathlib import Path
from typing import override

from file_conversor.config.locale import get_translation
from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager
from file_conversor.system import AbstractSystem, System


_ = get_translation()


class DnfPackageManager(AbstractPackageManager):
    """Package manager for Fedora / RHEL / CentOS (dnf/yum)."""

    def __init__(
        self,
        dependencies: dict[str, str],
        env: list[str | Path] | None = None,
    ) -> None:
        super().__init__(dependencies=dependencies, env=env)

    @override
    def _get_pkg_manager_installed(self) -> str | None:
        return shutil.which("dnf") or shutil.which("yum")

    @override
    def _get_supported_oses(self) -> set[AbstractSystem.Platform]:
        return {System.Platform.LINUX}

    @override
    def get_missing_dependencies(self) -> set[str]:
        # Skip entirely if dnf/yum is not available on this system
        if not self._get_pkg_manager_installed():
            return set()
        return super().get_missing_dependencies()

    @override
    def _get_cmd_install_pkg_manager(self) -> list[str]:
        raise RuntimeError("dnf/yum is a system package manager and cannot be installed by this tool.")

    @override
    def _post_install_pkg_manager(self) -> None:
        pass

    @override
    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        pkg_mgr_bin = self._get_pkg_manager_installed() or "dnf"
        return ["sudo", pkg_mgr_bin, "install", "-y", dependency]


__all__ = [
    "DnfPackageManager",
]
