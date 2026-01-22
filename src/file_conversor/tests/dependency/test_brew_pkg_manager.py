
# tests\backend\test_brew_pkg_manager.py

import pytest

from pathlib import Path

# user-provided imports
from file_conversor.dependency import BrewPackageManager

from file_conversor.system.abstract_system import AbstractSystem
from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestBrewPackageManager:
    def test_get_pkg_manager_installed(self) -> None:
        """Test BrewPackageManager when Homebrew is installed."""
        if AbstractSystem.Platform.get() not in (AbstractSystem.Platform.MACOS, AbstractSystem.Platform.LINUX):
            pytest.skip("Homebrew is only supported on macOS and Linux.")

        pkg_manager = BrewPackageManager(dependencies={"wget": "1.21.1"})
        assert Path(pkg_manager._get_pkg_manager_installed() or '').name == "brew"

    def test_get_supported_oses(self) -> None:
        """Test BrewPackageManager supported OSes."""
        pkg_manager = BrewPackageManager(dependencies={"wget": "1.21.1"})
        supported_oses = pkg_manager._get_supported_oses()
        assert AbstractSystem.Platform.LINUX in supported_oses
        assert AbstractSystem.Platform.MACOS in supported_oses

    def test_get_cmd_install_pkg_manager(self) -> None:
        """Test BrewPackageManager install command."""
        pkg_manager = BrewPackageManager(dependencies={"wget": "1.21.1"})
        cmd = pkg_manager._get_cmd_install_pkg_manager()
        assert len(cmd) > 0

    def test_get_cmd_install_dep(self) -> None:
        """Test BrewPackageManager install dependency command."""
        pkg_manager = BrewPackageManager(dependencies={"wget": "1.21.1"})
        cmd = pkg_manager._get_cmd_install_dep("wget")
        assert len(cmd) > 0
