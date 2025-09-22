# src\file_conversor\backend\git_backend.py

"""
This module provides functionalities for handling repositories using Git.
"""

from pathlib import Path
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import Environment, Log, get_translation

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager

from file_conversor.utils.validators import check_file_format

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class GitBackend(AbstractBackend):
    """
    GitBackend is a class that provides an interface for handling repositories using Git.
    """

    SUPPORTED_IN_FORMATS = {}

    SUPPORTED_OUT_FORMATS = {}

    EXTERNAL_DEPENDENCIES = {
        "git",
    }

    def check_repository(self, path: str | Path) -> Path:
        """
        Check if a given path is a Git repository.

        :param path: The path to check.

        :raises FileNotFoundError: if the path does not exist, or is not a .git repository
        """
        repo_path = Path(path).resolve()
        if not (repo_path / ".git").exists():
            raise FileNotFoundError(f"'{repo_path}' is not a git repository")
        return repo_path

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 
        :param verbose: Verbose logging. Defaults to False.      

        :raises RuntimeError: if calibre dependency is not found
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "git": "git"
                }),
                BrewPackageManager({
                    "git": "git"
                }),
            },
            install_answer=install_deps,
        )
        self._install_deps = install_deps
        self._verbose = verbose

        # check git
        self._git_bin = self.find_in_path("git")

    def checkout(
        self,
        dest_folder: str | Path,
        branch: str,
    ):
        """
        Checkout a branch in a Git repository.

        :param dest_folder: The destination folder.
        :param branch: The branch to checkout.
        """
        dest_folder = self.check_repository(dest_folder)

        # Execute command
        process = Environment.run(
            str(self._git_bin),
            "checkout",
            branch,
            cwd=dest_folder,
            stdout=None,
            stderr=None,
        )
        return process

    def clone_pull(
        self,
        repo_url: str,
        dest_folder: str | Path,
    ):
        """
        Clone or pull a Git repository.

        :param repo_url: The repository to clone or pull.
        :param dest_folder: The destination folder.
        """
        dest_path = Path(dest_folder).resolve()
        if (dest_path / ".git").exists():
            return self.pull(dest_folder=dest_folder)
        else:
            return self.clone(repo_url=repo_url, dest_folder=dest_folder)

    def clone(
        self,
        repo_url: str,
        dest_folder: str | Path,
    ):
        """
        Clone a Git repository.

        :param repo_url: The repository to clone.
        :param dest_folder: The destination folder.
        """
        dest_path = Path(dest_folder).resolve()
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if dest_path.exists() and any(dest_path.iterdir()):
            raise FileExistsError(f"'{dest_path}' already exists and is not empty")

        # Execute command
        print(f"{_('This might take a while (couple minutes, or hours) ...')}")

        process = Environment.run(
            str(self._git_bin),
            "clone",
            repo_url,
            str(dest_path),
            stdout=None,
            stderr=None,
        )
        return process

    def pull(
        self,
        dest_folder: str | Path,
    ):
        """
        Pull the latest changes from a Git repository.
        """
        dest_path = self.check_repository(dest_folder)

        # Execute command
        print(f"{_('This might take a while (couple minutes, or hours) ...')}")

        process = Environment.run(
            str(self._git_bin),
            "pull",
            cwd=dest_path,
            stdout=None,
            stderr=None,
        )
        return process
