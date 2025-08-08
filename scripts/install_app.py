
# scripts\install_app.py

import sysconfig
import argparse
import os
import platform
import subprocess
import sys
import tempfile

from pathlib import Path
from typing import Optional

WINDOWS = (platform.system() == "Windows")
print(f"PLATFORM: {platform.system()}")


class InstallationError(RuntimeError):
    def __init__(self, return_code: int = 0, log: Optional[str] = None):
        super().__init__()
        self.return_code = return_code
        self.log = log


class OSEnvPath:

    @staticmethod
    def set_path_process(*paths: Path):
        for path in paths:
            if not path.exists():
                raise InstallationError(return_code=1, log=f"Folder '{path}' not exists.")
            os.environ["PATH"] = str(path) + os.pathsep + os.environ["PATH"]

    @staticmethod
    def set_path_persistent(*paths: Path, scope: str):
        if WINDOWS:
            OSEnvPath.__set_path_persistent_nt(*paths, scope=scope)
        else:
            OSEnvPath.__set_path_persistent_posix(*paths, scope=scope)

    @staticmethod
    def __set_path_persistent_nt(*paths: Path, scope: str):
        # Read current PATH from user environment
        import winreg

        if scope == "machine":
            hive = winreg.HKEY_LOCAL_MACHINE
            key = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        elif scope == "user":
            hive = winreg.HKEY_CURRENT_USER
            key = r"Environment"
        else:
            raise InstallationError(return_code=1, log=f"Scope '{scope}' not valid")

        with winreg.OpenKey(hive, key, 0, winreg.KEY_READ) as k:
            try:
                current_path, _ = winreg.QueryValueEx(k, "PATH")
            except FileNotFoundError:
                current_path = ""

        # Only add if missing
        modified = False
        for path in paths:
            if str(path).lower() not in current_path.lower():
                current_path = str(path) + os.pathsep + current_path
                print(f"Added to PATH: {path}")
                modified = True
            else:
                print(f"Skipping '{path}'. Already in PATH.")

        # save
        if modified:
            with winreg.OpenKey(hive, key, 0, winreg.KEY_SET_VALUE) as k:
                winreg.SetValueEx(k, "PATH", 0, winreg.REG_EXPAND_SZ, current_path)
                print(f"PATH saved")

    @staticmethod
    def __set_path_persistent_posix(*paths: Path, scope: str):
        pass

    def __init__(self) -> None:
        super().__init__()
        os_prefix = 'nt' if WINDOWS else 'posix'
        self._paths = [
            Path(sysconfig.get_path('scripts', scheme=f"{os_prefix}")),
            Path(sysconfig.get_path('scripts', scheme=f"{os_prefix}_user")),
        ]

    def run(self):
        print(f"--- Setting Python scripts PATH ----")
        self.set_path_process(*self._paths)
        self.set_path_persistent(*self._paths, scope="user")
        print(f"--- END ----")


class Environment:
    def __init__(self) -> None:
        super().__init__()
        # str is for compatibility with subprocess.run on CPython <= 3.7 on Windows
        self._python = sys.executable
        if not Path(self._python).exists():
            raise InstallationError(return_code=1, log="Python binary not found")
        print(f"Python bin: {self._python}\n")
        osenv = OSEnvPath()
        osenv.run()

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
            self._env.pip("--version", stdout=subprocess.DEVNULL)
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
