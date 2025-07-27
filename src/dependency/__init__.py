# src\dependency\__init__.py

"""Module for package managers that provide external dependencies"""

from dependency.abstract_pkg_manager import AbstractPackageManager
from dependency.scoop_pkg_manager import ScoopPackageManager
from dependency.brew_pkg_manager import BrewPackageManager
