# tasks\_config.py

import hashlib
import os
import re
import shutil
import tomllib
import zipfile
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
README_PATH = Path("README.md")

GIT_RELEASE = f"v{PROJECT_VERSION}"

SCRIPTS_PATH = Path(f'scripts')
INSTALL_CHOCO = SCRIPTS_PATH / 'install_choco.ps1'
INSTALL_SCOOP = SCRIPTS_PATH / 'install_scoop.ps1'

DOCKER_REPOSITORY = "andreromano"
DOCKERFILE_PATH = Path(f"./dist/Dockerfile")

UNINSTALL_APP_WIN = Path("unins000.exe")

INSTALL_APP_WIN = Path(f"./dist/{PROJECT_NAME}-{GIT_RELEASE}-Win_x64.zip")
INSTALL_APP_LIN = Path(f"./dist/{PROJECT_NAME}-{GIT_RELEASE}-Lin_x64.zip")
INSTALL_APP_MAC = Path(f"./dist/{PROJECT_NAME}-{GIT_RELEASE}-Mac_x64.zip")

INSTALL_APP_WIN_EXE = Path(f"./dist/{PROJECT_NAME}-{GIT_RELEASE}-Win_x64-Installer.exe")
INSTALL_APP_WIN_EXE_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/releases/download/{GIT_RELEASE}/{INSTALL_APP_WIN_EXE.name}"
# INSTALL_APP_URL = f"https://raw.githubusercontent.com/andre-romano/{PROJECT_NAME}/refs/tags/{GIT_RELEASE}/{INSTALL_APP_PY.parent.name}/{INSTALL_APP_PY.name}"
# INSTALL_APP_URL = f"https://cdn.statically.io/gh/andre-romano/{PROJECT_NAME}@{GIT_RELEASE}/{INSTALL_APP.parent.name}/{INSTALL_APP.name}"
# INSTALL_APP_URL = f"https://cdn.jsdelivr.net/gh/andre-romano/{PROJECT_NAME}@{GIT_RELEASE}/{INSTALL_APP_PY.parent.name}/{INSTALL_APP_PY.name}"

INSTALL_APP_HASH = Path(f"./dist/checksum.sha256")
INSTALL_APP_HASH_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/releases/download/{GIT_RELEASE}/{INSTALL_APP_HASH.name}"

RELEASE_NOTES_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/releases/tag/{GIT_RELEASE}"
SOURCE_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/archive/refs/tags/{GIT_RELEASE}.zip"

LICENSE_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/blob/{GIT_RELEASE}/LICENSE"


def copy(src: Path, dst: Path):
    if not src.exists():
        raise FileNotFoundError(f"Src file '{src}' not found")
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


def get_url(url: str) -> bytes:
    response = requests.get(url)
    if not response.ok:
        raise RuntimeError(f"Cannot access url '{url}': {response.status_code} - {response.content}")
    return response.content


def get_hash(data: bytes | str | Path) -> str:
    if isinstance(data, (str, Path)):
        data = Path(data)
        if not data.exists():
            raise FileNotFoundError(f"{data}")
        try:
            data = Path(data).read_text()
            data.replace("\r", "")
            data = data.encode("utf-8")
        except:
            data = Path(data).read_bytes()
    return hashlib.sha256(data).hexdigest()


def get_remote_hash(url: str) -> str:
    return get_hash(get_url(url))


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


def parse_manifest_includes() -> list[str]:
    add_data_list = []
    if not MANIFEST_IN_PATH.exists():
        raise RuntimeError(f"Manifest file '{MANIFEST_IN_PATH}' not exists")
    for line in MANIFEST_IN_PATH.read_text().splitlines():
        match = re.match(r"^[\s]*include[\s]+(.+)", line)
        if match:
            add_data_list.extend([filepath.strip() for filepath in match.group(1).split()])
            continue

        match = re.match(r"^[\s]*recursive-include[\s]+([^\s]+)", line)
        if match:
            add_data_list.append(match.group(1).strip())
            continue
    return add_data_list


def append_to_PATH(paths: str | Path | list[str | Path]):
    path_list = [Path(paths)] if isinstance(paths, (str, Path)) else [Path(p) for p in paths]
    env_paths = os.environ["PATH"].split(os.pathsep)
    for path in path_list:
        path = path.resolve()
        if str(path) not in env_paths:
            env_paths.append(str(path))
    os.environ["PATH"] = os.pathsep.join(env_paths)


def remove_from_PATH(paths: str | Path | list[str | Path]):
    path_list = [Path(paths)] if isinstance(paths, (str, Path)) else [Path(p) for p in paths]
    env_paths = os.environ["PATH"].split(os.pathsep)
    for path in path_list:
        path = path.resolve()
        if str(path) in env_paths:
            env_paths.remove(str(path))
    os.environ["PATH"] = os.pathsep.join(env_paths)


def compress(src: Path, dst: Path):
    dst = dst.with_suffix(".zip")
    if not src.is_dir():
        raise ValueError(f"'{src}' is not a valid directory")

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(src):
            for file in files:
                file_path = Path(root) / file
                # keep relative path inside archive
                arcname = file_path.relative_to(src.parent)
                zipf.write(file_path, arcname)


def extract(src: Path, dst: Path):
    if not src.exists():
        raise FileNotFoundError(f"'{src}' does not exist")

    extract_to = Path(dst).resolve()
    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(src, "r") as zipf:
        zipf.extractall(extract_to)
