# src\file_conversor\config\environment.py

import subprocess
import shutil
import sys
import platformdirs
import platform

from importlib.resources import files
from importlib.metadata import version

from pathlib import Path
from enum import Enum

# user provided imports
from file_conversor.config.log import Log
from file_conversor.config.abstract_singleton_thread_safe import AbstractSingletonThreadSafe

# Get app config
logger = Log.get_instance().getLogger(__name__)


class Environment(AbstractSingletonThreadSafe):

    __APP_NAME = "file_conversor"

    class UserFolder(Enum):
        @classmethod
        def RUNTIME(cls) -> Path:
            return platformdirs.user_runtime_path().resolve()

        @classmethod
        def DATA(cls) -> Path:
            return platformdirs.user_data_path().resolve()

        @classmethod
        def CONFIG(cls) -> Path:
            return platformdirs.user_config_path().resolve()

        @classmethod
        def CACHE(cls) -> Path:
            return platformdirs.user_cache_path().resolve()

        @classmethod
        def LOG(cls) -> Path:
            return platformdirs.user_log_path().resolve()

        @classmethod
        def STATE(cls) -> Path:
            return platformdirs.user_state_path().resolve()

        @classmethod
        def MUSIC(cls) -> Path:
            return platformdirs.user_music_path().resolve()

        @classmethod
        def PICTURES(cls) -> Path:
            return platformdirs.user_pictures_path().resolve()

        @classmethod
        def VIDEOS(cls) -> Path:
            return platformdirs.user_videos_path().resolve()

        @classmethod
        def DOCUMENTS(cls) -> Path:
            return platformdirs.user_documents_path().resolve()

        @classmethod
        def DOWNLOADS(cls) -> Path:
            return platformdirs.user_downloads_path().resolve()

        @classmethod
        def DESKTOP(cls) -> Path:
            return platformdirs.user_desktop_path().resolve()

    class SiteFolder(Enum):
        @classmethod
        def RUNTIME(cls) -> Path:
            return platformdirs.site_runtime_path().resolve()

        @classmethod
        def DATA(cls) -> Path:
            return platformdirs.site_data_path().resolve()

        @classmethod
        def CONFIG(cls) -> Path:
            return platformdirs.site_config_path().resolve()

        @classmethod
        def CACHE(cls) -> Path:
            return platformdirs.site_cache_path().resolve()

    @classmethod
    def remove(cls, src: str | Path, globs: str = "*", remove_src: bool = True, no_exists_ok: bool = True):
        """
        Remove dir or file, using globs / wildcards

        :param src: Source folder/file to remove
        :param globs: Globs/wildcards to match files/folders to remove. Defaults to "*" (all files/folders).
        :param remove_src: If True, remove the source folder itself. Valid only if src is a directory. Defaults to True.
        :param no_exists_ok: Do not raise error if file/folder does not exist. Defaults to True.

        :raises FileNotFoundError: if file/folder does not exist and no_exists_ok is False
        """
        src_path = Path(src).resolve()
        if not src_path.exists():
            if no_exists_ok:
                return
            raise FileNotFoundError(f"Source '{src_path}' does not exist")

        if src_path.is_file():
            src_path.unlink()  # Remove single file
            return

        if src_path.is_dir():
            if remove_src:
                shutil.rmtree(src_path)
                return
            for path in src_path.glob(globs):
                logger.debug(f"Removing '{path}' ... ")
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()  # Remove single file

    @classmethod
    def copy(cls, src: Path | str, dst: Path | str, overwrite: bool = False):
        """Copy a file or folder."""
        src = Path(src).resolve()
        dst = Path(dst).resolve()
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            raise FileNotFoundError(f"Source '{src}' does not exist")
        if dst.exists():
            if not overwrite:
                raise FileExistsError(f"Destination '{dst}' already exists")
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    @classmethod
    def move(cls, src: Path | str, dst: Path | str, overwrite: bool = False):
        """Move a file or folder."""
        src = Path(src).resolve()
        dst = Path(dst).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Source '{src}' does not exist")
        if dst.exists():
            if not overwrite:
                raise FileExistsError(f"Destination '{dst}' already exists")
            cls.remove(dst, remove_src=True, no_exists_ok=True)
        shutil.move(str(src), str(dst))

    @classmethod
    def touch(cls, path: Path | str, mode: int = 0o644, exists_ok: bool = True):
        """Create an empty file."""
        path = Path(path).resolve()
        if path.exists() and not exists_ok:
            raise FileExistsError(f"File '{path}' already exists")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(mode=mode, exist_ok=exists_ok)

    @classmethod
    def get_system_platform(cls) -> str:
        """Get the current system platform."""
        return platform.system()

    @classmethod
    def get_executable(cls) -> str:
        """Get the executable path for this app's CLI."""
        res = ""

        exe = shutil.which(sys.argv[0]) if sys.argv else None
        if exe and not exe.endswith(".py"):
            res = rf'"{exe}"'
        else:
            python_exe = sys.executable
            res = rf'"{python_exe}" -m "{cls.get_app_name()}"'

        logger.debug(f"Executable cmd: {res}")
        return res

    @classmethod
    def get_resources_folder(cls) -> Path:
        """Get the absolute path of the included folders in pip."""
        files_obj = files(cls.get_app_name())
        res_path = Path(str(files_obj)).resolve()
        return res_path

    @classmethod
    def get_web_folder(cls) -> Path:
        web_path = cls.get_resources_folder() / ".web"
        # logger.debug(f"Web path: {web_path}")
        return web_path

    @classmethod
    def get_icons_folder(cls) -> Path:
        """Get the absolute path of the included folders in pip."""
        icons_path = cls.get_resources_folder() / ".icons"
        # logger.debug(f"Icons path: {icons_path}")
        return icons_path

    @classmethod
    def get_locales_folder(cls) -> Path:
        locales_path = cls.get_resources_folder() / ".locales"
        # logger.debug(f"Locales path: {locales_path}")
        return locales_path

    @classmethod
    def get_data_folder(cls) -> Path:
        """Get the app data folder."""
        data_path = cls.UserFolder.DATA() / cls.get_app_name()
        data_path.mkdir(parents=True, exist_ok=True)
        # logger.debug(f"App data path: {data_path}")
        return data_path

    @classmethod
    def get_version(cls) -> str:
        """Get the current version of the app."""
        return version(cls.get_app_name())

    @classmethod
    def get_app_icon(cls) -> Path:
        """Get the path to the app icon."""
        return cls.get_icons_folder() / "icon.ico"

    @classmethod
    def get_app_name(cls) -> str:
        """Get the app name."""
        return cls.__APP_NAME

    @classmethod
    def run_nowait(cls,
                   *cmd: str,
                   text: bool = True,
                   encoding: str | None = None,
                   env: dict | None = None,
                   cwd: str | Path | None = None,
                   stdout: int | None = subprocess.PIPE,
                   stderr: int | None = subprocess.STDOUT,
                   **kwargs,
                   ) -> subprocess.Popen:
        """
        Run a process within Python using a standardized API

        :param cmd: Command to run.
        :param text: Parse stdout/stderr as text. Defaults to True.
        :param encoding: Text encoding. Defaults to None (use system locale).
        :param env: Environment (variables, PATH, etc). Defaults to None (same as the current python process).
        :param cwd: Current working directory. Defaults to None (same as the current python process).
        :param stdint: Pass to stdin, or not. Defaults to ``None``.
        :param stdout: Capture stdout, or not. Defaults to ``subprocess.PIPE``.
        :param stderr: Capture stderr, or not. Defaults to ``subprocess.STDOUT``.
        """
        logger.debug(f"Starting process ...")
        logger.debug(f"{" ".join(cmd)}")

        process = subprocess.Popen(
            cmd,
            stdin=kwargs.get("stdin"),
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            env=env,
            text=text,
            encoding=encoding,

            # options
            close_fds=kwargs.get("close_fds", True),
            shell=kwargs.get("shell", False),
        )
        return process

    @classmethod
    def run(cls,
            *cmd: str,
            text: bool = True,
            encoding: str | None = None,
            env: dict | None = None,
            cwd: str | Path | None = None,
            stdout: int | None = subprocess.PIPE,
            stderr: int | None = subprocess.STDOUT,
            **kwargs,
            ) -> subprocess.CompletedProcess:
        """
        Run a process within Python, and wait for it to finish.

        :param cmd: Command to run.
        :param text: Parse stdout/stderr as text. Defaults to True.
        :param encoding: Text encoding. Defaults to None (use system locale).
        :param env: Environment (variables, PATH, etc). Defaults to None (same as the current python process).
        :param cwd: Current working directory. Defaults to None (same as the current python process).
        :param stdout: Capture stdout, or not. Defaults to ``subprocess.PIPE``.
        :param stderr: Capture stderr, or not. Defaults to ``subprocess.STDOUT``.

        :raises subprocess.CalledProcessError: if command failed (needs `wait` to work)
        :raises Exception: if communicate() failed (needs `wait` to work)
        """
        process = cls.run_nowait(
            *cmd,
            text=text,
            encoding=encoding,
            env=env,
            cwd=cwd,
            stdout=stdout,
            stderr=stderr,
            **kwargs,
        )
        try:
            output, error = process.communicate()
        except Exception:
            if process.poll() is None:
                process.kill()
                process.wait()
            raise

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=process.returncode,
                cmd=process.args,
                output=output,
                stderr=error,
            )

        return subprocess.CompletedProcess(
            args=process.args,
            returncode=process.returncode,
            stdout=output,
            stderr=error,
        )

    @classmethod
    def check_returncode(
        cls,
        process: subprocess.Popen | subprocess.CompletedProcess,
        out_lines: list[str] | None = None,
        err_lines: list[str] | None = None,
    ):
        """Raises subprocess.CalledProcessError if process.returncode != 0"""
        if process.returncode != 0:
            stdout: list[str] = (out_lines or []) + (process.stdout.readlines() if process.stdout else [])
            stderr: list[str] = (err_lines or []) + (process.stderr.readlines() if process.stderr else [])
            raise subprocess.CalledProcessError(
                returncode=process.returncode,
                cmd=process.args,
                output="\n".join([line.strip() for line in stdout if line.strip() != ""]),
                stderr="\n".join([line.strip() for line in stderr if line.strip() != ""]),
            )

    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "Environment",
]
