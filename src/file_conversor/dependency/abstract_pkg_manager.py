# src\file_conversor\dependency\abstract_pkg_manager.py

"""
This module provides functionalities for handling external backends.
"""

import shutil

from pathlib import Path
from typing import Any, Callable, Iterable, Protocol

from file_conversor.config import Environment, Log, get_translation
from file_conversor.system.abstract_system import AbstractSystem


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PackageManagerProtocol(Protocol):
    def _get_pkg_manager_installed(self) -> str | None:
        """ Returns package manager path, if already installed in system. """
        ...

    def _get_supported_oses(self) -> set[AbstractSystem.Platform]:
        """ Returns the package manager supported OSes. """
        ...

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        """ Returns the command to install the package manager in the system. """
        ...

    def _post_install_pkg_manager(self) -> None:
        """ Post installation steps after installing the package manager. """
        ...

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        """ Returns the command to install a dependency with the package manager. """
        ...


class AbstractPackageManager(PackageManagerProtocol):
    def __init__(self,
                 dependencies: dict[str, str],
                 env: list[str | Path] | None = None,
                 ) -> None:
        """
        Initializes package manager.

        :param dependencies: External dependencies to check. Format {``executable: dependency``}.        
        """
        super().__init__()
        self._dependencies = dependencies
        self._pre_install_dep_callbacks: list[Callable[[], Any]] = []
        self._post_install_dep_callbacks: list[Callable[[], Any]] = []
        self._set_env_path(env or [])

    def get_missing_dependencies(self) -> set[str]:
        """
        Check if external dependencies are installed.

        :return: Missing dependencies list.
        """
        missing_dependencies: set[str] = set()

        # check if executable exists
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
        """
        return self._get_pkg_manager_installed()

    def get_supported_oses(self) -> set[AbstractSystem.Platform]:
        """
        Gets the package manager supported OSes.

        :return: Set([PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_MACOS, ...])
        """
        return self._get_supported_oses()

    def install_pkg_manager(self) -> None:
        """
        Installs package manager for the current user.

        :return: package manager path if installation success, otherwise None .

        :raises RuntimeError: if package manager not supported in the OS.
        :raises RuntimeError: if pkg_mgr cannot be installed, or OS not supported.
        :raises subprocess.CalledProcessError: package manager could not be installed in system.
        """
        import subprocess

        if self.get_pkg_manager_installed():
            return
        self._check_os_supported()

        logger.info(f"{_('Installing package manager')} ...")
        logger.debug(f"{self._get_cmd_install_pkg_manager()}")
        subprocess.run(self._get_cmd_install_pkg_manager(), check=True)  # noqa: S603

        if self.get_pkg_manager_installed():
            raise RuntimeError(f"{_('Unable to install package manager in system')}.")
        self._post_install_pkg_manager()

    def install_dependencies(self, dependencies: Iterable[str]):
        """
        Installs dependencies with package manager.

        :param dependencies: External dependencies to install. Format [``dependency``, ...].

        :raises RuntimeError: package manager NOT installed in system, or OS not supported.
        :raises subprocess.CalledProcessError: dependency could not be installed in system.
        """
        import subprocess

        if not self.get_pkg_manager_installed():
            raise RuntimeError("Package manager NOT installed in system.")
        self._check_os_supported()

        logger.info(f"{_('Running pre-install dependency commands')} ...")
        for callback in self._pre_install_dep_callbacks:
            callback()

        logger.info(f"{_('Installing missing dependencies')} {list(dependencies)} ...")
        for dep in dependencies:
            subprocess.run(self._get_cmd_install_dep(dep), check=True)  # noqa: S603

        logger.info(f"{_('Running post-install dependency commands')} ...")
        for callback in self._post_install_dep_callbacks:
            callback()

    def add_pre_install_callback(self, callback: Callable[[], Any]):
        """ Adds a pre-install callback to run before installing dependencies. """
        self._pre_install_dep_callbacks.append(callback)

    def add_post_install_callback(self, callback: Callable[[], Any]):
        """ Adds a post-install callback to run after installing dependencies. """
        self._post_install_dep_callbacks.append(callback)

    def _set_env_path(self, env: list[Path | str]):
        if not env:
            logger.debug("No env PATH to set for pkg manager")
            return
        if AbstractSystem.Platform.get() not in self.get_supported_oses():
            return
        Environment.set_env_paths(env)

    def _check_os_supported(self):
        """ 
        Checks if package manager is supported in the current OS.

        :raises RuntimeError: if package manager not supported in the OS.
        """
        _platform = AbstractSystem.Platform.get()
        if _platform not in self.get_supported_oses():
            raise RuntimeError(f"{_("Package manager is not supported on")} '{_platform}'.")


__all__ = [
    "AbstractPackageManager",
]
