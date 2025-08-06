
# src\file_conversor\dependency\brew_pkg_manager.py

import os
import shutil

# user-provided imports
from file_conversor.system import PLATFORM_LINUX, PLATFORM_MACOS

from file_conversor.config.locale import get_translation
from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager

_ = get_translation()


class BrewPackageManager(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str]) -> None:
        super().__init__(dependencies)

    def _get_pkg_manager_installed(self):
        return shutil.which("brew")

    def _get_supported_oses(self) -> set[str]:
        return {PLATFORM_LINUX, PLATFORM_MACOS}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ['/bin/bash', '-c', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)']

    def _post_install_pkg_manager(self) -> None:
        possible_paths = [
            "/opt/homebrew/bin",               # macOS (Apple Silicon)
            "/usr/local/bin",                  # macOS (Intel)
            os.path.expanduser("~/.linuxbrew/bin"),  # Linux (Homebrew)
        ]

        for path in possible_paths:
            brew_path = shutil.which("brew", path=os.pathsep.join([path]))
            if brew_path:
                os.environ["PATH"] += os.pathsep + path
                break

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        pkg_mgr_bin = self._get_pkg_manager_installed()
        pkg_mgr_bin = pkg_mgr_bin if pkg_mgr_bin else "BREW_NOT_FOUND"
        return [pkg_mgr_bin, "install", dependency]
