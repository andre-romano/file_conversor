# tasks_modules\zip.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base, locales

if base.WINDOWS:
    INSTALL_APP_CURR = INSTALL_APP_WIN
elif base.LINUX:
    INSTALL_APP_CURR = INSTALL_APP_LIN
else:
    INSTALL_APP_CURR = INSTALL_APP_MAC

BUILD_DIR = Path(f"build/{PROJECT_NAME}")
REQUIREMENTS_TXT = BUILD_DIR / "requirements.txt"


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "dist",
        f"{BUILD_DIR}",
    ])


@task(pre=[mkdirs])
def clean_build(c: InvokeContext):
    remove_path(f"{BUILD_DIR}/*")


@task(pre=[mkdirs])
def clean_zip(c: InvokeContext):
    _config.remove_path(f"{INSTALL_APP_WIN}")
    _config.remove_path(f"{INSTALL_APP_LIN}")
    _config.remove_path(f"{INSTALL_APP_MAC}")


@task(pre=[clean_build])
def requirements(c: InvokeContext):
    print("[bold]Generating requirements.txt ...[/]")
    result = c.run(f"pdm export -f requirements -o \"{REQUIREMENTS_TXT}\" --prod --without-hashes")
    assert (result is not None) and (result.return_code == 0)
    if not REQUIREMENTS_TXT.exists():
        raise RuntimeError("Cannot generate 'requirements.txt'")
    print("[bold]Generating requirements.txt ... [/][bold green]OK[/]")


@task(pre=[requirements])
def requirements_download(c: InvokeContext):
    print(f"[bold] Downloading deps to {BUILD_DIR} ... [/]")

    cmd_list = [
        "pip",
        "install",
        "-r", f"{REQUIREMENTS_TXT}",
        "-t", f"{BUILD_DIR}",
        "--no-warn-script-location",
    ]
    print(rf"$ {cmd_list}")
    result = c.run(" ".join(cmd_list))
    assert (result is not None) and (result.return_code == 0)

    print(f"[bold] Downloading deps to {BUILD_DIR} ... [/][bold green]OK[/]")


@task(pre=[requirements_download, locales.build])
def copy_src_folder(c: InvokeContext):
    print(f"[bold] Copying src/ to {BUILD_DIR} ... [/]")

    src_path = Path("src") / PROJECT_NAME
    dest_path = BUILD_DIR / PROJECT_NAME
    _config.copy(src=src_path, dst=dest_path)

    if not dest_path.exists():
        raise RuntimeError(f"Cannot copy '{src_path}' to '{dest_path}'")

    print(f"[bold] Copying src/ to {BUILD_DIR} ... [/][bold green]OK[/]")


@task(pre=[copy_src_folder])
def create_shim(c: InvokeContext):
    print(f"[bold] Creating shim file ... [/]")

    init_path = BUILD_DIR / f"__init__.py"
    init_path.touch(exist_ok=True)
    assert init_path.exists()

    main_path = BUILD_DIR / f"__main__.py"
    main_path.write_text(rf"""
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
        # Windows
        ps1_launcher_file = BUILD_DIR / f"_{PROJECT_NAME}.ps1"
        ps1_launcher_file.write_text(rf"""$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
                                     
$pythonPath = ""

function Install-Python-Scoop {{
    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {{
        Write-Warning "Scoop is not installed. Installing Scoop ..."
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    }}
    if (Get-Command scoop -ErrorAction SilentlyContinue) {{
        scoop install -y python
    }}
    else {{
        Write-Error "Scoop not found. Please install Python manually and ensure it's in your PATH."
        exit 1
    }}
}}

function Install-Python-Choco {{
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {{
        Write-Warning "Chocolatey is not installed. Installing Chocolatey ..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }}
    if (Get-Command choco -ErrorAction SilentlyContinue) {{
        choco install -y python
    }}
    else {{
        Write-Error "Chocolatey not found. Please install Python manually and ensure it's in your PATH."
        exit 1
    }}
}}

function Get-Python-Installed {{
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) {{ return $cmd }}
    $cmd = Get-Command python3 -ErrorAction SilentlyContinue
    if ($cmd) {{ return $cmd }}
    return $null
}}

$pythonCmd = Get-Python-Installed
if (-not $pythonCmd) {{
    Write-Warning "Python is not installed or not found in PATH."
    Write-Warning "Installing Python ..."

    # $true se estiver rodando como admin
    $IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    if ($IsAdmin) {{
        Write-Output "Admin mode, using Chocolatey to install Python ..."
        Install-Python-Choco
    }}
    else {{
        Write-Output "Normal user mode, using Scoop to install Python ..."
        Install-Python-Scoop
    }}
}}

$pythonCmd = Get-Python-Installed
if (-not $pythonCmd) {{
    Write-Error "Python is not installed or not found in PATH."
    exit 1
}}

$pythonPath = $pythonCmd.Path

& $pythonPath "$scriptDir\__main__.py" @args
""", encoding="utf-8")
        assert ps1_launcher_file.exists()
        print(f"{ps1_launcher_file.name} contents:\n{ps1_launcher_file.read_text(encoding='utf-8')}")

        # Create a .bat file to launch the PowerShell script
        shim_file = BUILD_DIR / f"{PROJECT_NAME}.bat"
        shim_file.write_text(rf"""@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0\{ps1_launcher_file.name}" %*
""", encoding="utf-8")
    else:
        # Linux/MacOS
        shim_file = BUILD_DIR / f"{PROJECT_NAME}.sh"
        shim_file.write_text(rf"""#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found in PATH" >&2
    exit 1
fi

$PYTHON_CMD "$SCRIPT_DIR/__main__.py" "$@"
""", encoding="utf-8")
    assert shim_file.exists()
    print(f"{shim_file.name} contents:\n{shim_file.read_text(encoding='utf-8')}")
    shim_file.chmod(0o755)  # Make it executable
    assert os.access(shim_file, os.X_OK), f"Cannot make '{shim_file}' executable"

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
    result = c.run(f"{SHIM_FILE.resolve()} --version")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Checking .ZIP ... [/][bold green]OK[/]")
