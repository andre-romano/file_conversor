# src\file_conversor\backend\abstract_backend.py

"""
This module provides functionalities for handling external backends.
"""

import os
import platform
import shutil
import typer

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
            logger.warning(f"[bold]{_("Missing dependencies detected")}[/]: {", ".join(missing_deps)}")

            # install package manager, if not present already
            pkg_mgr_bin = pkg_mgr.get_pkg_manager_installed()
            if pkg_mgr_bin:
                logger.info(f"Package manager found in '{pkg_mgr_bin}'")
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
                        logger.info(f"Package manager installed in '{result}'")
                    logger.info(f"[bold]{_("Package Manager Installation")}[/]: [green]{_("SUCCESS")}[/]")

            # install missing dependencies
            if install_answer is None:
                user_prompt = typer.confirm(
                    _(f"Install missing dependencies for the current user?"),
                    default=True,
                )
            else:
                user_prompt = install_answer
            if user_prompt:
                pkg_mgr.install_dependencies(missing_deps)
                logger.info(f"[bold]{_("External Dependencies Installation")}[/]: [green]{_("SUCCESS")}[/]")
