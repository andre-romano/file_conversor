#!/usr/bin/env python3

import re
import sys
import tomllib


def get_version_parts(version: str):
    version_match = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?$", version)
    if not version_match:
        raise RuntimeError(f"Invalid version format: '{version}'")
    major = int(version_match.group(1))
    minor = int(version_match.group(2))
    patch = int(version_match.group(3)) if version_match.group(3) else 0
    return major, minor, patch


def sub_version(version: str, amount: int = 1):
    major, minor, patch = get_version_parts(version)
    if patch >= amount:
        patch -= amount
    elif minor > 0:
        minor -= 1
        patch = 99  # assuming max patch version is 99
    elif major > 0:
        major -= 1
        minor = 99  # assuming max minor version is 99
        patch = 99
    else:
        raise RuntimeError(f"Cannot subtract {amount} from version '{version}'")
    return major, minor, patch


def add_version(version: str, amount: int = 1):
    major, minor, patch = get_version_parts(version)
    patch += amount
    if patch >= 100:  # assuming max patch version is 99
        patch = 0
        minor += 1
        if minor >= 100:  # assuming max minor version is 99
            minor = 0
            major += 1
    return major, minor, patch


def get_python_version():
    min_version = ""
    max_version = ""
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    if "project" in pyproject and "requires-python" in pyproject["project"]:
        requires_python: str = pyproject["project"]["requires-python"].split(",")
        for req_orig in requires_python:
            req = req_orig.strip()
            if req.startswith(">="):
                min_version = req[2:].strip()
            elif req.startswith(">"):
                min_version = req[1:].strip()
                major, minor, patch = add_version(min_version)
                min_version = f"{major}.{minor}.{patch}"
            elif req.startswith("<="):
                max_version = req[2:].strip()
            elif req.startswith("<"):
                max_version = req[1:].strip()
                major, minor, patch = sub_version(max_version)
                max_version = f"{major}.{minor}.{patch}"
    return min_version, max_version


if __name__ == "__main__":
    min_py, max_py = get_python_version()
    print(f"min={min_py}")
    print(f"max={max_py}")
    sys.exit(0)
