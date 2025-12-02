# src\file_conversor\backend\git_backend.py

"""
This module provides functionalities for handling repositories using Git.
"""

from pathlib import Path
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.http_backend import HttpBackend, NetworkError

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

    @staticmethod
    def get_download_url(
        user_name: str,
        repo_name: str,
        file_path: str | Path,
        branch: str = "",
    ):
        """Get the download URL for a file in a GitHub repository.

        :param user_name: The GitHub username or organization name.
        :param repo_name: The name of the repository.
        :param file_path: The path to the file in the repository.        
        :param branch: The branch name. If not provided, the default branch will be used.
        """
        file_path = Path(file_path)
        request_url = f"https://raw.githubusercontent.com/{user_name}/{repo_name}/{branch}/{file_path.as_posix()}"
        return request_url

    @staticmethod
    def get_info_api(
        user_name: str,
        repo_name: str,
        path: str | Path = "",
        branch: str = "",
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

        :param user_name: The GitHub username or organization name.
        :param repo_name: The name of the repository.
        :param path: The path to the file or directory in the repository. Defaults to the root directory.
        :param branch: The branch name. If not provided, the default branch will be used.

        :return: A dictionary containing information about the file or directory.

        :raises RuntimeError: if the GitHub API request fails
        """
        http_backend = HttpBackend.get_instance(verbose=False)
        res = http_backend.get_json(
            url=f"https://api.github.com/repos/{user_name}/{repo_name}/contents/{path}",
            params={"ref": branch} if branch else None,
        )
        if isinstance(res, dict) and res.get("status", "200") != "200":
            raise NetworkError(f"{_('Failed to retrieve info from GitHub API')}: {res.get('status', '200')} - {res.get('message', '')}")
        if isinstance(res, dict):
            return [res]
        elif isinstance(res, list):
            return res
        else:
            raise NetworkError(f"{_('Failed to retrieve info from GitHub API')}: {type(res)}")

    @staticmethod
    def check_repository(path: str | Path) -> Path:
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


__all__ = [
    "GitBackend",
]
