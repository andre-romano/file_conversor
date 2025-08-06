# src\file_conversor\dependency\__init__.py

"""Module for package managers that provide external dependencies"""

from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager
from file_conversor.dependency.scoop_pkg_manager import ScoopPackageManager
from file_conversor.dependency.brew_pkg_manager import BrewPackageManager
