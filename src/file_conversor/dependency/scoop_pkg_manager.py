
# src/dependency/scoop_pkg_manager.py

import os
import shutil

# user-provided imports
from file_conversor.system import PLATFORM_WINDOWS

from file_conversor.config.locale import get_translation

from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager

_ = get_translation()


class ScoopPackageManager(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str]) -> None:
        super().__init__(dependencies)

    def _get_pkg_manager_installed(self) -> str | None:
        return shutil.which("scoop")

    def _get_supported_oses(self) -> set[str]:
        return {PLATFORM_WINDOWS}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            "iwr -useb get.scoop.sh | iex"
        ]

    def _post_install_pkg_manager(self) -> None:
        # update current PATH (current process path)
        scoop_shims = os.path.expandvars(r"%USERPROFILE%\scoop\shims")
        os.environ["PATH"] += os.pathsep + scoop_shims

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        pkg_mgr_bin = self._get_pkg_manager_installed()
        pkg_mgr_bin = pkg_mgr_bin if pkg_mgr_bin else "SCOOP_NOT_FOUND"
        return [pkg_mgr_bin, "install", dependency, "-k"]
