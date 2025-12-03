# src\file_conversor\dependency\abstract_pkg_manager.py

"""
This module provides functionalities for handling external backends.
"""

import os
import platform
import shutil
import subprocess

from rich import print
from typing import Any, Callable, Iterable
from pathlib import Path

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AbstractPackageManager:
    NOT_IMPLEMENTED_ERROR_MSG = "Method not overloaded."

    def __init__(self,
                 dependencies: dict[str, str],
                 env: list[str | Path] | None = None,
                 ) -> None:
        """
        Initializes package manager.

        :param dependencies: External dependencies to check. Format {``executable: dependency``}.        
        """
        super().__init__()
        self._os_type = platform.system()
        self._dependencies = dependencies
        self._env = env
        self._pre_install_dep_callbacks: list[Callable[[], Any]] = []
        self._post_install_dep_callbacks: list[Callable[[], Any]] = []

    def check_dependencies(self) -> set[str]:
        """
        Check if external dependencies are installed.

        :return: Missing dependencies list.
        """
        missing_dependencies: set[str] = set()

        # check if executable exists
        self._set_env_path()
        for executable, dependency in self._dependencies.items():
            found_exe = shutil.which(executable)
            if not found_exe:
                logger.warning(f"ABSTRACT PKG MANAGER - {_('Executable')} '{executable}' {_('not found')}. {_('Marking dependency')} '{dependency}' {_('for installation')}.")
                missing_dependencies.add(dependency)

        # missing dependencies
        return missing_dependencies

    def get_pkg_manager_installed(self) -> str | None:
        """
        Checks if the package manager is already installed in system.

        :return: package manager path if installed, otherwise None

        :raises RuntimeError: if package manager not supported in the OS.
        """
        if self._os_type not in self.get_supported_oses():
            raise RuntimeError(f"{_("Package manager is not supported on")} '{self._os_type}'.")
        return self._get_pkg_manager_installed()

    def get_supported_oses(self) -> set[str]:
        """
        Gets the package manager supported OSes.

        :return: Set([PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_MACOS, ...])
        """
        return self._get_supported_oses()

    def install_pkg_manager(self) -> str | None:
        """
        Installs package manager for the current user.

        :return: package manager path if installation success, otherwise None .

        :raises RuntimeError: if package manager not supported in the OS.
        :raises RuntimeError: package manager already installed in system.
        :raises subprocess.CalledProcessError: package manager could not be installed in system.
        """
        if self.get_pkg_manager_installed():
            raise RuntimeError("Package manager already installed in system.")
        logger.info(f"{_('Installing package manager')} ...")
        logger.debug(f"{self._get_cmd_install_pkg_manager()}")
        subprocess.run(self._get_cmd_install_pkg_manager(), check=True)
        self._post_install_pkg_manager()
        return self.get_pkg_manager_installed()

    def install_dependencies(self, dependencies: Iterable[str]):
        """
        Installs dependencies with package manager.

        :param dependencies: External dependencies to install. Format [``dependency``, ...].

        :raises RuntimeError: package manager NOT installed in system.
        :raises subprocess.CalledProcessError: dependency could not be installed in system.
        """
        if not self.get_pkg_manager_installed():
            raise RuntimeError("Package manager NOT installed in system.")
        logger.info(f"{_('Running pre-install dependency commands')} ...")
        for callback in self._pre_install_dep_callbacks:
            callback()
        logger.info(f"{_('Installing missing dependencies')} {list(dependencies)} ...")
        for dep in dependencies:
            subprocess.run(self._get_cmd_install_dep(dep), check=True)
        logger.info(f"{_('Running post-install dependency commands')} ...")
        for callback in self._post_install_dep_callbacks:
            callback()

    def add_pre_install_callback(self, callback: Callable[[], Any]):
        """ Adds a pre-install callback to run before installing dependencies. """
        self._pre_install_dep_callbacks.append(callback)

    def add_post_install_callback(self, callback: Callable[[], Any]):
        """ Adds a post-install callback to run after installing dependencies. """
        self._post_install_dep_callbacks.append(callback)

    def _set_env_path(self):
        if not self._env:
            logger.debug("No env PATH to set for pkg manager")
            return
        # check if needs to add path
        env_paths = os.environ["PATH"].split(os.pathsep)
        for path_str in self._env:
            path_str = str(path_str)
            if path_str in env_paths:
                logger.debug(f"Skipping path '{path_str}'. Already in ENV")
                continue
            env_paths.append(path_str)
        os.environ["PATH"] = os.pathsep.join(env_paths)

    def _get_pkg_manager_installed(self) -> str | None:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def _get_supported_oses(self) -> set[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def _post_install_pkg_manager(self) -> None:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


__all__ = [
    "AbstractPackageManager",
]
