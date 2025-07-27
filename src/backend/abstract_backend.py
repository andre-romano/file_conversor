# src/backend/abstract_backend.py

"""
This module provides functionalities for handling external backends.
"""

import platform
import subprocess
import typer

from typing import Iterable
from rich import print

# user-provided imports
from dependency import AbstractPackageManager
from config.locale import get_translation

_ = get_translation()


class AbstractBackend:
    """
    Class that provides an interface for handling internal/external backends.
    """

    @staticmethod
    def dump_streams(process: subprocess.Popen | None, stdout=True, stderr=True) -> str:
        """Dumps stdout and/or stderr into a string"""
        res = ""
        if not process:
            return res
        if process.stderr:
            for line in process.stderr:
                res += line
        if process.stdout:
            for line in process.stdout:
                res += line
        return res

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
        pkg_managers = pkg_managers if pkg_managers else set()

        # identify OS and package manager
        os_type = platform.system()
        for pkg_mgr in pkg_managers:
            if os_type not in pkg_mgr.get_supported_oses():
                continue
            # supported pkg manager found, proceed to check for dependencies
            missing_deps = pkg_mgr.check_dependencies()
            if not missing_deps:
                # no dependencies missing, skip
                break
            print(f"[bold]{_("Missing dependencies detected")}[/]: {", ".join(missing_deps)}")

            # install package manager, if not present already
            pkg_mgr_bin = pkg_mgr.get_pkg_manager_installed()
            if pkg_mgr_bin:
                print(f"Package manager found in '{pkg_mgr_bin}'")
            else:
                user_prompt: bool
                if install_answer is None:
                    user_prompt = typer.confirm(
                        _("Install package manager for the current user?"),
                        default=True,
                    )
                else:
                    user_prompt = install_answer
                if user_prompt:
                    result = pkg_mgr.install_pkg_manager()
                    if result:
                        print(f"Package manager installed in '{result}'")
                    print_result = f"[green]{_("SUCCESS")}[/]" if result else f"[red]{_("FAILED")}[/]"
                    print(f"[bold]{_("Package Manager Installation")}[/]: {print_result}")

            # install missing dependencies
            if install_answer is None:
                user_prompt = typer.confirm(
                    _(f"Install missing dependencies for the current user?"),
                    default=True,
                )
            else:
                user_prompt = install_answer
            if user_prompt:
                result = pkg_mgr.install_dependencies(missing_deps)
                print_result = f"[green]{_("SUCCESS")}[/]" if result else f"[red]{_("FAILED")}[/]"
                print(f"[bold]{_("External Dependencies Installation")}[/]: {print_result}")
