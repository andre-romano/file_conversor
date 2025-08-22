# tasks\_config.py

import hashlib
import shutil
import tomllib
import requests

from invoke.context import Context as InvokeContext
from typing import Any, Iterable
from pathlib import Path

from rich import print

# Read version from pyproject.toml
PYPROJECT: dict[str, Any]
with open("pyproject.toml", "rb") as f:
    PYPROJECT = tomllib.load(f)

# CONSTANTS
PROJECT_AUTHORS: list[str] = list(str(a["name"]) if isinstance(a, dict) else str(a) for a in PYPROJECT["project"]["authors"])
PROJECT_KEYWORDS: list[str] = PYPROJECT["project"]["keywords"]

PROJECT_NAME = str(PYPROJECT["project"]["name"])
PROJECT_VERSION = str(PYPROJECT["project"]["version"])
PROJECT_DESCRIPTION = str(PYPROJECT["project"]["description"])

PROJECT_TITLE = str(PYPROJECT["tool"]["myproject"]["title"])

PROJECT_HOMEPAGE = f"https://github.com/andre-romano/{PROJECT_NAME}"

ICONS_PATH = Path(PYPROJECT["tool"]["myproject"]["icons_path"])
I18N_PATH = Path(PYPROJECT["tool"]["myproject"]["locales_path"])

ICON_APP = Path(rf"{ICONS_PATH}/icon.ico")
I18N_TEMPLATE = Path(rf"{I18N_PATH}/messages.pot")

MANIFEST_IN_PATH = Path("MANIFEST.in")
RELEASE_NOTES_PATH = Path("RELEASE_NOTES.md")

GIT_RELEASE = f"v{PROJECT_VERSION}"

SCRIPTS_PATH = Path(f'scripts')
INSTALL_CHOCO = SCRIPTS_PATH / 'install_choco.ps1'
INSTALL_SCOOP = SCRIPTS_PATH / 'install_scoop.ps1'

UNINSTALL_APP = Path("unins000.exe")

INSTALL_APP = Path(f"./dist/{PROJECT_NAME}-{GIT_RELEASE}-Win_x64-Installer.exe")
INSTALL_APP_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/releases/download/{GIT_RELEASE}/{INSTALL_APP.name}"
# INSTALL_APP_URL = f"https://raw.githubusercontent.com/andre-romano/{PROJECT_NAME}/refs/tags/{GIT_RELEASE}/{INSTALL_APP_PY.parent.name}/{INSTALL_APP_PY.name}"
# INSTALL_APP_URL = f"https://cdn.statically.io/gh/andre-romano/{PROJECT_NAME}@{GIT_RELEASE}/{INSTALL_APP.parent.name}/{INSTALL_APP.name}"
# INSTALL_APP_URL = f"https://cdn.jsdelivr.net/gh/andre-romano/{PROJECT_NAME}@{GIT_RELEASE}/{INSTALL_APP_PY.parent.name}/{INSTALL_APP_PY.name}"

INSTALL_APP_HASH = INSTALL_APP.with_suffix(".sha256")
INSTALL_APP_HASH_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/releases/download/{GIT_RELEASE}/{INSTALL_APP_HASH.name}"


def copy(src: Path, dst: Path):
    print(f"Copying '{src}' => '{dst}' ...", end="")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        shutil.copy2(src=src, dst=dst)
    elif src.is_dir():
        # If the directory exists, remove it first to avoid errors
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src=src, dst=dst)
    assert dst.exists()
    print(f"[bold green]OK[/]")


def remove_path(path_pattern: str):
    """Remove dir or file, using globs / wildcards"""
    for path in Path('.').glob(path_pattern):
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


def mkdir(dirs: Iterable):
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


def get_hash(data: bytes | str | Path) -> str:
    if isinstance(data, (str, Path)):
        try:
            data = Path(data).read_text()
            data.replace("\r", "")
            data = data.encode("utf-8")
        except:
            data = Path(data).read_bytes()
    return hashlib.sha256(data).hexdigest()


def get_remote_hash(url: str) -> str:
    response = requests.get(url)
    if not response.ok:
        raise RuntimeError(f"Cannot access url '{url}': {response.status_code} - {response.content}")
    return get_hash(response.content)


def verify_with_sha256_file(sha_file: Path):
    for line in sha_file.read_text().splitlines():
        try:
            expected, name = line.strip().split()
        except:
            continue
        print(f"'{name}': ", end="")
        actual = get_hash(sha_file.parent / name)
        if actual.lower() != expected.lower():
            print(f"[bold red]FAILED[/]")
            raise RuntimeError(f"Hashes for '{name}' dont match. Expected: {expected}. Actual: {actual}")
        print(f"[bold green]OK[/]")
