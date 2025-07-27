# src/dependency/abstract_pkg_manager.py

"""
This module provides functionalities for handling external backends.
"""

import platform
import shutil

import subprocess
from typing import Any, Iterable
from rich import print

# user-provided imports
from config.locale import get_translation
from utils.rich import get_progress_bar

_ = get_translation()


class AbstractPackageManager:

    def __init__(self, dependencies: dict[str, str]) -> None:
        """
        Initializes package manager.

        :param dependencies: External dependencies to check. Format {``executable: dependency``}.
        """
        super().__init__()
        self._dependencies = dependencies
        self._os_type = platform.system()

    def check_dependencies(self) -> set[str]:
        """
        Check if external dependencies are installed.

        :return: Missing dependencies list.
        """
        missing_dependencies = set([])

        # check if executable exists
        for executable, dependency in self._dependencies.items():
            found_exe = shutil.which(executable)
            if not found_exe:
                print(f"[bold white]ABSTRACT PKG MANAGER[/]: {_('Executable')} '{executable}' {_('not found')}. {_('Marking dependency')} '{dependency}' {_('for installation')}.")
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

        :return: Set(["Windows", "Linux", "Darwin", ...])
        """
        return self._get_supported_oses()

    def install_pkg_manager(self) -> str | None:
        """
        Installs package manager for the current user.

        :return: package manager path if installation success, otherwise None .

        :raises RuntimeError: if package manager not supported in the OS.
        :raises RuntimeError: package manager already installed in system.
        """
        if self.get_pkg_manager_installed():
            raise RuntimeError("Package manager already installed in system.")
        try:
            print(f"{_('Installing package manager')} ...")
            subprocess.run(self._get_cmd_install_pkg_manager(), check=True)
            self._post_install_pkg_manager()
            return self.get_pkg_manager_installed()
        except subprocess.CalledProcessError as e:
            print(f"[bold red]{_('Failed to install package manager')}[/]: {e}")
            return None

    def install_dependencies(self, dependencies: Iterable[str]) -> bool:
        """
        Installs dependencies with package manager.

        :param dependencies: External dependencies to install. Format [``dependency``, ...].

        :return:  True if installation success.

        :raises RuntimeError: package manager NOT installed in system.
        """
        res = True
        if not self.get_pkg_manager_installed():
            raise RuntimeError("Package manager NOT installed in system.")
        for dep in dependencies:
            try:
                subprocess.run(self._get_cmd_install_dep(dep), check=True)
            except subprocess.CalledProcessError as e:
                print(f"[bold red]{_('Failed to install dependency')} '{dep}': {e}")
                res = False
        return res

    def _get_pkg_manager_installed(self) -> str | None:
        raise NotImplementedError("Method not overloaded.")

    def _get_supported_oses(self) -> set[str]:
        raise NotImplementedError("Method not overloaded.")

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        raise NotImplementedError("Method not overloaded.")

    def _post_install_pkg_manager(self) -> None:
        raise NotImplementedError("Method not overloaded.")

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        raise NotImplementedError("Method not overloaded.")
