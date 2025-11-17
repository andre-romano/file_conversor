#!/usr/bin/env python3

import sys
import toml
import re


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
    MIN = ""
    MAX = ""
    pyproject = toml.load("pyproject.toml")
    if "project" in pyproject:
        if "requires-python" in pyproject["project"]:
            requires_python = pyproject["project"]["requires-python"].split(",")
            for req in requires_python:
                req = req.strip()
                if req.startswith(">="):
                    MIN = req[2:].strip()
                elif req.startswith(">"):
                    MIN = req[1:].strip()
                    major, minor, patch = add_version(MIN)
                    MIN = f"{major}.{minor}.{patch}"
                elif req.startswith("<="):
                    MAX = req[2:].strip()
                elif req.startswith("<"):
                    MAX = req[1:].strip()
                    major, minor, patch = sub_version(MAX)
                    MAX = f"{major}.{minor}.{patch}"
    return MIN, MAX


if __name__ == "__main__":
    min_py, max_py = get_python_version()
    print(f"min={min_py}")
    print(f"max={max_py}")
    sys.exit(0)
