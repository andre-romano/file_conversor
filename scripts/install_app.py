
# scripts\install_app.py

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile

from pathlib import Path
from typing import Optional

WINDOWS = platform.system().startswith("Windows")
LINUX = platform.system().startswith("Linux")
MACOS = platform.system().startswith("Darwin")


class InstallationError(RuntimeError):
    def __init__(self, return_code: int = 0, log: Optional[str] = None):
        super().__init__()
        self.return_code = return_code
        self.log = log


class Environment:
    def __init__(self) -> None:
        super().__init__()
        # str is for compatibility with subprocess.run on CPython <= 3.7 on Windows
        self._python = shutil.which("python.exe" if WINDOWS else "python") or (
            shutil.which("python3.exe" if WINDOWS else "python3")
        )
        if not self._python:
            raise InstallationError(return_code=1, log="Python binary not found in PATH")
        print(f"Python bin: {self._python}")

    @staticmethod
    def run(*args, **kwargs) -> subprocess.CompletedProcess:
        print(f"$ {' '.join(args)}")
        completed_process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            **kwargs,
        )
        print(completed_process.stdout.strip() + "\n")
        if completed_process.returncode != 0:
            raise InstallationError(
                return_code=completed_process.returncode,
                log=completed_process.stdout,
            )
        return completed_process

    def python(self, *args, **kwargs) -> subprocess.CompletedProcess:
        return self.run(self._python, *args, **kwargs)

    def pip(self, *args, **kwargs) -> subprocess.CompletedProcess:
        return self.python("-m", "pip", *args, **kwargs)


class Installer:
    def __init__(self,
                 env: Environment,
                 app_name: str,
                 version: str | None = None,
                 force: bool | None = None,
                 install: bool | None = None,
                 uninstall: bool | None = None,
                 ) -> None:
        super().__init__()
        self._env = env
        self._app_name = app_name
        self._version = version
        self._force = force or False
        self._install = install or False
        self._uninstall = uninstall or False
        self._ensure_pip()
        self._update_pip()

    def _ensure_pip(self) -> None:
        try:
            self._env.pip("--version")
        except:
            print("Attempting to fix 'pip' (ensurepip) ...")
            self._env.python("-m", "ensurepip", "--upgrade")

    def _update_pip(self) -> None:
        print("Updating 'pip' ...")
        self._env.pip("install", "--upgrade", "pip")

    def _install_app(self) -> None:
        print(f"Installing {self._app_name} {f'v{self._version}' if self._version else ''} ...")
        specs = f"{self._app_name}=={self._version}" if self._version else self._app_name
        self._env.pip("install", specs)
        self._post_install_app()

    def _post_install_app(self):
        print("Post-install steps ...")
        self._env.run(self._app_name, "win", "install-menu")

    def _pre_uninstall_app(self):
        print("Pre-uninstall steps ...")
        self._env.run(self._app_name, "win", "uninstall-menu")

    def _uninstall_app(self) -> None:
        self._pre_uninstall_app()
        print(f"Uninstalling {self._app_name} {f'v{self._version}' if self._version else ''} ...")
        self._env.pip("uninstall", self._app_name, "-y")

    def run(self):
        if not self._install and not self._uninstall:
            raise InstallationError(return_code=1, log=f"No operation mode informed. Requires -i or -u flags.")
        if self._install and self._uninstall:
            raise InstallationError(return_code=1, log=f"More than one operation mode informed: -i and -u flags")

        if self._install:
            self._install_app()
        elif self._uninstall:
            self._uninstall_app()

        print("Installation SUCCESS")
        return 0


def main():
    try:
        app_name = "file_conversor"

        parser = argparse.ArgumentParser(
            description=f"Installs the latest (or given) version of {app_name}"
        )
        parser.add_argument("-v", "--version", dest="version",
                            help="install named version",
                            )
        parser.add_argument("-f", "--force", dest="force",
                            help="install on top of existing version",
                            action="store_true",
                            default=False,
                            )
        parser.add_argument("-i", "--install", dest="install",
                            help=f"install {app_name}",
                            action="store_true",
                            default=False,
                            )
        parser.add_argument("-u", "--uninstall", dest="uninstall",
                            help=f"uninstall {app_name}",
                            action="store_true",
                            default=False,
                            )

        args = parser.parse_args()
        installer = Installer(
            env=Environment(),
            app_name=app_name,
            version=args.version,
            force=args.force,
            install=args.install,
            uninstall=args.uninstall,
        )
        return installer.run()
    except Exception as e:
        if not isinstance(e, InstallationError):
            print(repr(e))

        print("\nERROR: Installation failed.")

        import traceback
        _, path = tempfile.mkstemp(
            suffix=".log",
            prefix=f"{app_name}-installer-error-",
            dir=str(Path.cwd()),
            text=True,
        )
        print(f"See {path} for error logs.")
        tb = "".join(traceback.format_tb(e.__traceback__))
        ret_code = 1
        if isinstance(e, InstallationError):
            text = f"Return Code: {e.return_code}\nLog: {e.log}\nTraceback:\n\n{tb}"
            ret_code = e.return_code
        else:
            text = f"{repr(e)}\nTraceback:\n\n{tb}"
            ret_code = 1
        Path(path).write_text(text)
        return ret_code


if __name__ == "__main__":
    sys.exit(main())
