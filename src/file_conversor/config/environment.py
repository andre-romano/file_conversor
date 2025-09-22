
import subprocess
import shutil
import sys
import time

from importlib.resources import files

from pathlib import Path

# user provided imports
from file_conversor.config.log import Log

# Get app config
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class Environment:

    __instance = None

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
    def get_executable(cls) -> str:
        """Get the executable path for this app's CLI."""
        res = ""

        exe = shutil.which(sys.argv[0]) if sys.argv else None
        if exe and not exe.endswith(".py"):
            res = rf'"{exe}"'
        else:
            python_exe = sys.executable
            main_py = Path(rf"{cls.get_resources_folder()}/__main__.py")
            res = rf'"{python_exe}" "{main_py}"'

        logger.debug(f"Executable cmd: {res}")
        return res

    @classmethod
    def get_resources_folder(cls) -> Path:
        """Get the absolute path of the included folders in pip."""
        res_path = Path(str(files("file_conversor"))).resolve()
        return res_path

    @classmethod
    def get_data_folder(cls) -> Path:
        data_path = cls.get_resources_folder() / ".data"
        logger.debug(f"Data path: {data_path}")
        return data_path

    @classmethod
    def get_icons_folder(cls) -> Path:
        """Get the absolute path of the included folders in pip."""
        icons_path = cls.get_resources_folder() / ".icons"
        logger.debug(f"Icons path: {icons_path}")
        return icons_path

    @classmethod
    def get_locales_folder(cls) -> Path:
        locales_path = cls.get_resources_folder() / ".locales"
        logger.debug(f"Locales path: {locales_path}")
        return locales_path

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

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
