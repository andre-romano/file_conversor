# tasks\_config.py

import hashlib
import sys
import os
import re
import shutil
import tomllib
import zipfile
import requests

from invoke.context import Context as InvokeContext
from typing import Any, Iterable
from pathlib import Path
from email.utils import formatdate

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

PROJECT_ENTRYPOINTS: list[str] = list(PYPROJECT["project"]["scripts"].values())

PROJECT_HOMEPAGE = f"https://github.com/andre-romano/{PROJECT_NAME}"
CHOCO_PKG_REPO_URL = f"https://github.com/andre-romano/{PROJECT_NAME}"

ICONS_PATH = Path(PYPROJECT["tool"]["myproject"]["icons_path"])
I18N_PATH = Path(PYPROJECT["tool"]["myproject"]["locales_path"])

ICON_APP = Path(rf"{ICONS_PATH}/icon.ico")
I18N_TEMPLATE = Path(rf"{I18N_PATH}/messages.pot")

MANIFEST_IN_PATH = Path("MANIFEST.in")
RELEASE_NOTES_PATH = Path("RELEASE_NOTES.md")
README_PATH = Path("README.md")

GIT_RELEASE = f"v{PROJECT_VERSION}"

CACHE_DIR = Path(".cache")

SCRIPTS_PATH = Path(f'scripts')
INSTALL_PYTHON = SCRIPTS_PATH / 'install_python.ps1'
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

ICON_URL = f"http://rawcdn.githack.com/andre-romano/{PROJECT_NAME}/master/{str(ICONS_PATH).replace("\\", "/")}/icon.png"

LICENSE_URL = f"https://github.com/andre-romano/{PROJECT_NAME}/blob/{GIT_RELEASE}/LICENSE"

PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
EMBEDPY_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"


def move(src: Path, dst: Path):
    if not src.exists():
        raise FileNotFoundError(f"Src file '{src}' not found")
    print(f"Moving '{src}' => '{dst}' ...", end="")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src=src, dst=dst)
    assert dst.exists()
    print(f"[bold green]OK[/]")


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


def remove_path(path_pattern: str, base_path: Path = Path(), dry_run: bool = False, verbose: bool = False):
    """Remove dir or file, using globs / wildcards"""
    if not verbose:
        print(f"Cleaning '{base_path}/{path_pattern}' ... ", end="")
    for path in base_path.rglob(path_pattern):
        if not path.exists():
            pass
        if verbose:
            print(f"Cleaning '{path}' ... ", end="")
        if not dry_run:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()  # Remove single file
            if path.exists():
                raise RuntimeError(f"Cannot remove dir / file '{path}'")
        if verbose:
            print("[bold green]OK[/]")
    if not verbose:
        print("[bold green]OK[/]")


def mkdir(dirs: Iterable):
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


def get_dir_size(path: Path | str) -> tuple[str, float]:
    """
    Get the total size of a directory and its contents.

    :return: (human-readable string, size in bytes).
    """
    path = Path(path)
    total: float = 0.0 if path.is_dir() else float(path.stat().st_size)
    total += sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
    # Return size in a human-readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if total < 1024:
            return (f"{total:.2f} {unit}", total)
        total /= 1024
    return (f"{total:.2f} PB", total)


def get_url(url: str, cache: bool = True, **kwargs) -> tuple[bytes, Path | None]:
    cache_file: Path | None = None
    if cache:
        cache_file = CACHE_DIR / hashlib.sha256(url.encode("utf-8")).hexdigest()
        print(f"Using cache file: {cache_file} ({url})")

    headers = kwargs.get("headers", {})
    if cache_file and cache_file.exists():
        mtime = cache_file.stat().st_mtime  # posix timestamp
        headers["If-Modified-Since"] = formatdate(timeval=mtime, usegmt=True)

    if "headers" in kwargs:
        del kwargs["headers"]
    if "stream" in kwargs:
        del kwargs["stream"]

    print(f"Accessing url '{url}' ... ", end="")
    response = requests.get(url, headers=headers, stream=True, **kwargs)
    print(f"[bold blue]{response.status_code}[/]")

    if not response.ok:
        raise RuntimeError(f"Cannot access url '{url}': {response.status_code} - {response.content}")
    if cache_file and response.status_code == 304:
        print("Cached version is up-to-date.")
        return (cache_file.read_bytes(), cache_file)
    else:
        print("A newer version is available.")
        if cache_file:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_bytes(response.content)
            print(f"Updated {cache_file}")
        return (response.content, cache_file if cache_file else None)


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


def get_remote_hash(url: str, cache: bool = True, **kwargs) -> str:
    return get_hash(get_url(url, cache=cache, **kwargs)[0])


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


def compress(src: Path, dst: Path, compress: int = zipfile.ZIP_DEFLATED, compress_level: int = 9):
    dst = dst.with_suffix(".zip")
    if not src.is_dir():
        raise ValueError(f"'{src}' is not a valid directory")

    with zipfile.ZipFile(dst, "w", compression=compress, compresslevel=compress_level) as zipf:
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


def git_commit_push(c: InvokeContext, path: Path | str, message: str):
    path = Path(path).resolve()
    result = c.run(f'git status', hide=True)
    assert (result is not None) and (result.return_code == 0)

    if path.name not in result.stdout:
        print(f"[bold] Skipping commit: file {path.name} not changed. [/]")
        return

    result = c.run(f'git add "{path}"', hide=True)
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f'git commit -m "{message}"', hide=True)
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f'git push', hide=True)
    assert (result is not None) and (result.return_code == 0)


def get_whl_file(path: str | Path = "dist"):
    path = Path(path)
    for whl in path.glob(f"{PROJECT_NAME}-*.whl"):
        if PROJECT_VERSION in str(whl):
            return whl
    raise RuntimeError(f"WHL file not found in '{path}'")
