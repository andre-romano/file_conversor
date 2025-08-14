
# scripts\install_app.py

import re
import shutil
import argparse
import os
import sys
import platform
import subprocess
import tempfile

from pathlib import Path
from typing import Optional

WINDOWS = (platform.system() == "Windows")
print(f"PLATFORM: {platform.system()}")

IS_ADMIN = False
if WINDOWS:
    try:
        import ctypes
        IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        pass
else:
    IS_ADMIN = (os.geteuid() == 0)  # type: ignore
print(f"IS_ADMIN: {'yes' if IS_ADMIN else 'no'}\n")


class InstallationError(RuntimeError):
    def __init__(self, return_code: int = 0, log: Optional[str] = None):
        super().__init__()
        self.return_code = return_code
        self.log = log


class Environment:
    def __init__(self) -> None:
        super().__init__()
        # str is for compatibility with subprocess.run on CPython <= 3.7 on Windows
        self._python = sys.executable
        if not Path(self._python).exists():
            raise InstallationError(return_code=1, log="Python binary not found")
        print(f"Python bin: {self._python}\n")

    @staticmethod
    def remove_path(*patterns: str):
        """Remove dir or file, using globs / wildcards"""
        for pattern in patterns:
            for path in Path('.').glob(pattern):
                if not path.exists():
                    pass
                print(f"Cleaning '{path}' ... ", end="")
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()  # Remove single file
                if path.exists():
                    raise RuntimeError(f"Cannot remove dir / file '{path}'")
                print("[bold green]OK[/]")

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

    def pdm(self, *args, **kwargs) -> subprocess.CompletedProcess:
        return self.python("-m", "pdm", *args, **kwargs)

    def find_shim(self, app: str) -> Path:
        shim_path = "Scripts" if WINDOWS else "bin"
        REGEX_APP = re.compile(rf"^{app}(\.(bin|sh|cmd|bat|exe))?$")
        for path in Path(f'.venv/{shim_path}').rglob("*"):
            match = REGEX_APP.match(path.name)
            if match:
                path = path.resolve()
                print(f"Found shim: '{path}'")
                return path
        raise InstallationError(return_code=1, log=f"Shim for '{app}' not found")


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
            self._env.pip("--version", stdout=subprocess.DEVNULL)
        except:
            print("Attempting to fix 'pip' (ensurepip) ...")
            self._env.python("-m", "ensurepip", "--upgrade")

    def _update_pip(self) -> None:
        print("Updating 'pip' ...")
        self._env.pip("install", "--upgrade", "pip")

    def _pre_install_app(self):
        print("Pre-install steps ...")
        self._env.pip("install", "pdm")
        self._env.pdm("init", "--no-git", "--name", f"{self._app_name}_local", "--project-version", self._version, "--license", "not_set", "--non-interactive")

    def _install_app(self) -> None:
        print(f"Installing {self._app_name} {f'v{self._version}' if self._version else ''} ...")
        specs = f"{self._app_name}=={self._version}" if self._version else self._app_name
        self._env.pdm("add", specs)

    def _post_install_app(self):
        app_shim = self._env.find_shim(self._app_name)
        print("Post-install steps ...")
        if WINDOWS:
            self._env.run(str(app_shim), "win", "install-menu",)

    def _pre_uninstall_app(self):
        app_shim = self._env.find_shim(self._app_name)
        print("Pre-uninstall steps ...")
        if WINDOWS:
            self._env.run(str(app_shim), "win", "uninstall-menu",)

    def _uninstall_app(self) -> None:
        print(f"Uninstalling {self._app_name} {f'v{self._version}' if self._version else ''} ...")
        self._env.remove_path(rf"*")

    def _post_uninstall_app(self):
        print("Post-uninstall steps ...")

    def run(self):
        if not self._install and not self._uninstall:
            raise InstallationError(return_code=1, log=f"No operation mode informed. Requires -i or -u flags.")
        if self._install and self._uninstall:
            raise InstallationError(return_code=1, log=f"More than one operation mode informed: -i and -u flags")

        if self._install:
            self._pre_install_app()
            self._install_app()
            self._post_install_app()
            print("Install SUCCESS")
        elif self._uninstall:
            self._pre_uninstall_app()
            self._uninstall_app()
            self._post_uninstall_app()
            print("Uninstall SUCCESS")
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

        print("\nERROR: (Un)Install failed.")

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
