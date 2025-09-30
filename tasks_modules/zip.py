# tasks_modules\zip.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base, pypi

if base.WINDOWS:
    INSTALL_APP_CURR = INSTALL_APP_WIN
elif base.LINUX:
    INSTALL_APP_CURR = INSTALL_APP_LIN
else:
    INSTALL_APP_CURR = INSTALL_APP_MAC

BUILD_DIR = Path(f"build") / PROJECT_NAME
SITE_PACKAGES = BUILD_DIR / "lib" / "site-packages"

SHIM_FILE = BUILD_DIR / f"{PROJECT_NAME}.bat"
if not base.WINDOWS:
    SHIM_FILE = BUILD_DIR / f"{PROJECT_NAME}.sh"


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "dist",
        f"{BUILD_DIR}",
        f"{SITE_PACKAGES}",
    ])


@task(pre=[mkdirs])
def clean_build(c: InvokeContext):
    remove_path(f"{BUILD_DIR}/*")


@task(pre=[mkdirs])
def clean_zip(c: InvokeContext):
    _config.remove_path(f"{INSTALL_APP_WIN}")
    _config.remove_path(f"{INSTALL_APP_LIN}")
    _config.remove_path(f"{INSTALL_APP_MAC}")


@task(pre=[clean_build, pypi.build])
def requirements_download(c: InvokeContext):
    print(f"[bold] Downloading deps to {BUILD_DIR} ... [/]")

    cmd_list = [
        "pip",
        "install",
        "-t", f"{SITE_PACKAGES}",
        "--no-warn-script-location",
        f"{_config.get_whl_file().resolve()}",
    ]
    print(rf"$ {cmd_list}")
    result = c.run(" ".join(cmd_list))
    assert (result is not None) and (result.return_code == 0)

    print(f"[bold] Downloading deps to {BUILD_DIR} ... [/][bold green]OK[/]")


@task(pre=[requirements_download])
def create_shim(c: InvokeContext):
    print(f"[bold] Creating shim file ... [/]")

    init_path = SITE_PACKAGES / f"__init__.py"
    init_path.touch(exist_ok=True)
    assert init_path.exists()

    main_path = SITE_PACKAGES / f"__main__.py"
    main_path.write_text(rf"""#!/usr/bin/python
import sys
from pathlib import Path

src_dir = Path(__file__).resolve().parents[0]
sys.path.insert(0, f"{{src_dir}}")
print(f"Added to sys.path: '{{src_dir}}'")

from {PROJECT_NAME}.__main__ import main
if __name__ == '__main__':
    main()
""", encoding="utf-8")
    assert main_path.exists()
    print(f"{main_path.name} contents:\n{main_path.read_text(encoding='utf-8')}")

    if base.WINDOWS:
        # Create a .bat file to launch the PowerShell script
        SHIM_FILE.write_text(rf"""@echo off

set SCRIPT_DIR=%~dp0
set APP_ENTRYPOINT=%SCRIPT_DIR%\\{main_path.relative_to(BUILD_DIR)}

for /f "usebackq tokens=3*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul`) do set "PATH_MACHINE=%%B"
for /f "usebackq tokens=3*" %%A in (`reg query "HKCU\Environment" /v Path 2^>nul`) do set "PATH_USER=%%B"

set "PATH=%PATH_MACHINE%;%PATH_USER%;%PATH%"                             

python "%APP_ENTRYPOINT%" %*
""", encoding="utf-8")
    else:
        # Linux/MacOS
        SHIM_FILE.write_text(rf"""#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
APP_ENTRYPOINT="$SCRIPT_DIR/{main_path.relative_to(BUILD_DIR)}"

python "$APP_ENTRYPOINT" "$@"
""", encoding="utf-8")
    assert SHIM_FILE.exists()
    print(f"{SHIM_FILE.name} contents:\n{SHIM_FILE.read_text(encoding='utf-8')}")

    SHIM_FILE.chmod(0o755)  # Make it executable
    assert os.access(SHIM_FILE, os.X_OK), f"Cannot make '{SHIM_FILE}' executable"

    print(f"[bold] Creating shim file ... [/][bold green]OK[/]")


@task(pre=[clean_zip, create_shim],)
def build(c: InvokeContext):
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/]")
    _config.compress(src=BUILD_DIR, dst=INSTALL_APP_CURR)
    if not INSTALL_APP_CURR.exists():
        raise RuntimeError(f"'{INSTALL_APP_CURR}' not found")
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/][bold green]OK[/]")


@task(pre=[build,],)
def extract_app(c: InvokeContext):
    print(rf'[bold] Extracting {INSTALL_APP_CURR} ... [/]')
    _config.remove_path(str(BUILD_DIR))
    _config.extract(src=INSTALL_APP_CURR, dst=BUILD_DIR.parent)
    if not BUILD_DIR.exists():
        raise RuntimeError(f"'{BUILD_DIR}' not found")
    print(rf'[bold] Extracting {INSTALL_APP_CURR} ... [/][bold green]OK[/]')


@task(pre=[extract_app,])
def check(c: InvokeContext):
    print("[bold] Checking .ZIP ... [/]")
    SHIM_FILE = BUILD_DIR / (f"{PROJECT_NAME}.bat" if base.WINDOWS else f"{PROJECT_NAME}.sh")
    if not base.WINDOWS:
        c.run(f"chmod +rx {SHIM_FILE.resolve()}")
    result = c.run(f"{SHIM_FILE.resolve()} --version")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Checking .ZIP ... [/][bold green]OK[/]")
