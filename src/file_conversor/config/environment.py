
import subprocess
import shutil
import sys

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
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
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
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
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
    def check_returncode(cls, process: subprocess.Popen | subprocess.CompletedProcess):
        """Raises subprocess.CalledProcessError if process.returncode != 0"""
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=process.returncode,
                cmd=process.args,
                output="\n".join(process.stdout.readlines()) if process.stdout else "",
                stderr="\n".join(process.stderr.readlines()) if process.stderr else "",
            )

    def __init__(self) -> None:
        super().__init__()
