# src\file_conversor\backend\git_backend.py

"""
This module provides functionalities for handling repositories using Git.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.http_backend import HttpBackend, NetworkError
from file_conversor.config import Environment, Log, get_translation
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class GitBackend(AbstractBackend):
    """
    GitBackend is a class that provides an interface for handling repositories using Git.
    """

    @dataclass
    class RepositoryDataModel:
        user_name: str
        repo_name: str
        branch: str = ""

    class SupportedInFormats(Enum):
        pass

    class SupportedOutFormats(Enum):
        pass

    EXTERNAL_DEPENDENCIES: set[str] = {
        "git",
    }

    @staticmethod
    def get_download_url(
        repository: RepositoryDataModel,
        file_path: Path,
    ):
        """Get the download URL for a file in a GitHub repository.

        :param repository: The repository data model containing user_name, repo_name, and branch.
        :param file_path: The path to the file in the repository.
        """
        request_url = f"https://raw.githubusercontent.com/{repository.user_name}/{repository.repo_name}/{repository.branch}/{file_path.as_posix()}"
        return request_url

    @staticmethod
    def get_info_api(
        repository: RepositoryDataModel,
        path: Path = Path(),
    ) -> list[dict[str, Any]]:
        """
        Get information about a file or directory in a GitHub repository using the GitHub API.

        return [{
            "name": "filename",
            "path": "path/to/filename",
            "sha": "53098f771f720bf80a8e05ac53f6c281da6cf2b5",
            "size": number | 0 (if a directory),
            "url": "https://api.github.com/repos/<user>/<repo>/contents/.gitmodules?ref=<branch>",
            "html_url": "https://github.com/<user>/<repo>/blob/<branch>/.gitmodules",
            "download_url": "https://raw.githubusercontent.com/<user>/<repo>/<branch>/.gitmodules",
            "type": "file"|"dir",
        }]

        :param repository: The repository data model containing user_name, repo_name, and branch.
        :param path: The path to the file or directory in the repository. Defaults to the root directory.

        :return: A dictionary containing information about the file or directory.

        :raises RuntimeError: if the GitHub API request fails
        """
        http_backend = HttpBackend(verbose=False)
        res = http_backend.get_json(
            url=f"https://api.github.com/repos/{repository.user_name}/{repository.repo_name}/contents/{path.as_posix()}",
            params={"ref": repository.branch} if repository.branch else None,
        )
        if isinstance(res, dict) and res.get("status", "200") != "200":  # pyright: ignore[reportUnknownMemberType]
            raise NetworkError(f"{_('Failed to retrieve info from GitHub API')}: {res.get('status', '200')} - {res.get('message', '')}")  # pyright: ignore[reportUnknownMemberType]
        if isinstance(res, dict):
            return [res]
        if isinstance(res, list):
            return res  # pyright: ignore[reportUnknownVariableType]
        raise NetworkError(f"{_('Failed to retrieve info from GitHub API')}: {type(res)}")

    @staticmethod
    def check_repository(path: Path) -> Path:
        """
        Check if a given path is a Git repository.

        :param path: The path to check.

        :raises FileNotFoundError: if the path does not exist, or is not a .git repository
        """
        path = path.resolve()
        if not (path / ".git").exists():
            raise FileNotFoundError(f"'{path}' is not a git repository")
        return path

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
        dest_folder: Path,
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
        dest_folder: Path,
    ):
        """
        Clone or pull a Git repository.

        :param repo_url: The repository to clone or pull.
        :param dest_folder: The destination folder.
        """
        dest_folder = dest_folder.resolve()
        if (dest_folder / ".git").exists():
            return self.pull(dest_folder=dest_folder)
        return self.clone(repo_url=repo_url, dest_folder=dest_folder)

    def clone(
        self,
        repo_url: str,
        dest_folder: Path,
    ):
        """
        Clone a Git repository.

        :param repo_url: The repository to clone.
        :param dest_folder: The destination folder.
        """
        dest_folder = dest_folder.resolve()
        dest_folder.parent.mkdir(parents=True, exist_ok=True)

        if dest_folder.exists() and any(dest_folder.iterdir()):
            raise FileExistsError(f"'{dest_folder}' already exists and is not empty")

        # Execute command
        print(f"{_('This might take a while (couple minutes, or hours) ...')}")

        process = Environment.run(
            str(self._git_bin),
            "clone",
            repo_url,
            str(dest_folder),
            stdout=None,
            stderr=None,
        )
        return process

    def pull(
        self,
        dest_folder: Path,
    ):
        """
        Pull the latest changes from a Git repository.
        """
        dest_folder = self.check_repository(dest_folder)

        # Execute command
        print(f"{_('This might take a while (couple minutes, or hours) ...')}")

        process = Environment.run(
            str(self._git_bin),
            "pull",
            cwd=dest_folder,
            stdout=None,
            stderr=None,
        )
        return process


__all__ = [
    "GitBackend",
]
