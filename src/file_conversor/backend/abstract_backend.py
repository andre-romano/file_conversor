# src\file_conversor\backend\abstract_backend.py

"""
This module provides functionalities for handling external backends.
"""

import os
import platform
import shutil
import typer

from typing import Iterable
from pathlib import Path
from rich import print

# user-provided imports
from file_conversor.dependency import AbstractPackageManager

from file_conversor.config import Log
from file_conversor.config.locale import get_translation

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AbstractBackend:
    """
    Class that provides an interface for handling internal/external backends.
    """

    @staticmethod
    def find_in_path(name: str | Path) -> Path:
        """
        Finds name path in PATH env

        :return: Path for name

        :raises FileNotFoundError: if name not found
        """
        path_str = shutil.which(name)
        if not path_str:
            raise FileNotFoundError(f"'{name}' {_('not found in PATH environment')}")
        path = Path(path_str).resolve()
        logger.info(f"'{name}' {_('found')}: {path}")
        return path

    @staticmethod
    def check_file_exists(filename: str | Path):
        """
        Check if `filename` exists

        :raises FileNotFoundError: if file not found
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"{_("File")} '{filename}' {_("not found")}")

    def __init__(
        self,
        pkg_managers: set[AbstractPackageManager] | None = None,
        install_answer: bool | None = None,
    ):
        """
        Initialize the abstract backend.

        Checks if external dependencies are installed, and if not, install them.

        :param pkg_managers: Pkg managers configured to install external dependencies. Defaults to None (no external dependency required).
        :param install_answer: If True, do not ask user to install dependency (auto install). If False, do not install missing dependencies. If None, ask user for action. Defaults to None.

        :raises RuntimeError: Cannot install missing dependency or unknown OS detected.
        """
        super().__init__()
        self._pkg_managers = pkg_managers if pkg_managers else set()
        self._install_answer = install_answer

        self.verify_missing_deps()

    def verify_missing_deps(self):
        """
        Verify and install missing external dependencies, if they are not installed.
        :raises RuntimeError: Cannot install missing dependency.
        """
        # identify OS and package manager
        os_type = platform.system()
        for pkg_mgr in self._pkg_managers:
            if os_type not in pkg_mgr.get_supported_oses():
                continue

            # supported pkg manager found, proceed to check for dependencies
            missing_deps = self._check_missing_deps(pkg_mgr)
            if not missing_deps:
                continue

            # install package manager, if not present already
            self._check_pkg_manager_installed(pkg_mgr)

            # install missing dependencies
            self._install_missing_deps(pkg_mgr, missing_deps)

    def _check_missing_deps(self, pkg_mgr: AbstractPackageManager) -> set[str]:
        """
        Check for missing dependencies using the provided package manager.

        :param pkg_mgr: Package manager to use for checking dependencies.
        :return: Set of missing dependencies.
        """
        missing_deps = pkg_mgr.check_dependencies()
        if missing_deps:
            logger.warning(f"[bold]{_("Missing dependencies detected")}[/]: {", ".join(missing_deps)}")
        return missing_deps

    def _check_pkg_manager_installed(self, pkg_mgr: AbstractPackageManager):
        """
        Check if package manager is installed, and if not, install it.

        :param pkg_mgr: Package manager to check/install.
        :raises RuntimeError: Cannot install missing package manager.
        """
        pkg_mgr_bin = pkg_mgr.get_pkg_manager_installed()
        if pkg_mgr_bin:
            logger.info(f"Package manager found in '{pkg_mgr_bin}'")
            return

        logger.warning(f"{_('Package manager not found, installing it ...')}.")
        user_prompt = self._install_answer
        if user_prompt is None:
            user_prompt = typer.confirm(
                _("Install package manager for the current user?"),
                default=True,
            )
        if not user_prompt:
            raise RuntimeError(_("Cannot install missing package manager"))

        pkg_mgr_path = pkg_mgr.install_pkg_manager()
        logger.info(f"Package manager installed in '{pkg_mgr_path}'")
        logger.info(f"[bold]{_("Package Manager Installation")}[/]: [green]{_("SUCCESS")}[/]")

    def _install_missing_deps(self, pkg_mgr: AbstractPackageManager, missing_deps: Iterable[str]):
        """
        Install missing dependencies using the provided package manager.

        :param pkg_mgr: Package manager to use for installation.
        :param missing_deps: Set of missing dependencies to install.
        :raises RuntimeError: Cannot install missing dependencies.
        """

        user_prompt = self._install_answer
        if user_prompt is None:
            user_prompt = typer.confirm(
                _("Install missing dependencies for the current user?"),
                default=True,
            )
        if not user_prompt:
            raise RuntimeError(_("Cannot install missing dependencies"))

        pkg_mgr.install_dependencies(missing_deps)
        logger.info(f"[bold]{_("External Dependencies Installation")}[/]: [green]{_("SUCCESS")}[/]")


__all__ = [
    "AbstractBackend",
]
