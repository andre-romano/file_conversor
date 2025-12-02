
# src\file_conversor\dependency\brew_pkg_manager.py

import os
import shutil

from pathlib import Path

# user-provided imports
from file_conversor.system import _PLATFORM_LINUX, _PLATFORM_MACOS

from file_conversor.config.locale import get_translation
from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager

_ = get_translation()


class BrewPackageManager(AbstractPackageManager):
    def __init__(self,
                 dependencies: dict[str, str],
                 env: list[str | Path] | None = None,
                 ) -> None:
        self._fix_path()
        super().__init__(
            dependencies=dependencies,
            env=env,
        )

    def _fix_path(self):
        possible_paths = [
            "/opt/homebrew/bin",               # macOS (Apple Silicon)
            "/usr/local/bin",                  # macOS (Intel)
            "/home/linuxbrew/.linuxbrew/bin",  # Linux (Homebrew)
            os.path.expanduser("~/.linuxbrew/bin"),  # Linux (Homebrew)
        ]
        for path in possible_paths:
            brew_path = shutil.which("brew", path=os.pathsep.join([path]))
            if brew_path:
                os.environ["PATH"] += os.pathsep + path
                break

    def _get_pkg_manager_installed(self):
        return shutil.which("brew")

    def _get_supported_oses(self) -> set[str]:
        return {_PLATFORM_LINUX, _PLATFORM_MACOS}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ['bash', '-c', 'export HOMEBREW_NO_INSTALL_CLEANUP=1 ; curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash']

    def _post_install_pkg_manager(self) -> None:
        self._fix_path()

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        pkg_mgr_bin = self._get_pkg_manager_installed()
        pkg_mgr_bin = pkg_mgr_bin if pkg_mgr_bin else "BREW_NOT_FOUND"
        return ["bash", "-c", f'export HOMEBREW_NO_INSTALL_CLEANUP=1 ; "{pkg_mgr_bin}" install "{dependency}"']


__all__ = [
    "BrewPackageManager",
]
