
# src\file_conversor\__init__.py

"""
This is the root of the package.
It is used to initialize the package and can contain package-level variables or imports.
"""

# Read version from pyproject.toml
import tomllib
from typing import Any

PYPROJECT: dict[str, Any]
with open("pyproject.toml", "rb") as f:
    PYPROJECT = tomllib.load(f)

__VERSION__ = str(PYPROJECT["project"]["version"])
