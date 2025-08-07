# tasks\_config.py

import hashlib
import shutil
import tomllib
import requests

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

ICONS_PATH = str(PYPROJECT["tool"]["myproject"]["icons_path"])
I18N_PATH = str(PYPROJECT["tool"]["myproject"]["locales_path"])

I18N_TEMPLATE = f"{I18N_PATH}/messages.pot"

GIT_RELEASE = f"v{PROJECT_VERSION}"

SCRIPTS_PATH = str(f'scripts')
INSTALL_CHOCO = Path(f'{SCRIPTS_PATH}/install_choco.ps1')
INSTALL_SCOOP = Path(f'{SCRIPTS_PATH}/install_scoop.ps1')

INSTALL_APP_PY = Path(f"{SCRIPTS_PATH}/install_app.py")
INSTALL_APP_URL = f"https://cdn.jsdelivr.net/gh/andre-romano/{PROJECT_NAME}@master/{INSTALL_APP_PY.parent.name}/{INSTALL_APP_PY.name}"


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


def get_remote_hash(url):
    response = requests.get(url)
    return hashlib.sha256(response.content).hexdigest()
