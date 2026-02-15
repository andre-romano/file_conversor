
# tests\backend\test_scoop_pkg_manager.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.dependency import ScoopPackageManager
from file_conversor.system.abstract_system import AbstractSystem


class TestScoopPackageManager:
    def test_get_pkg_manager_installed(self) -> None:
        """Test ScoopPackageManager when Scoop is installed."""
        if AbstractSystem.Platform.get() != AbstractSystem.Platform.WINDOWS:
            pytest.skip("Scoop is only supported on Windows.")
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        if pkg_manager._get_pkg_manager_installed():  # pyright: ignore[reportPrivateUsage]
            assert Path(pkg_manager._get_pkg_manager_installed() or '').with_suffix("").name == "scoop"  # pyright: ignore[reportPrivateUsage]

    def test_get_supported_oses(self) -> None:
        """Test ScoopPackageManager supported OSes."""
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        supported_oses = pkg_manager._get_supported_oses()  # pyright: ignore[reportPrivateUsage]
        assert AbstractSystem.Platform.WINDOWS in supported_oses

    def test_get_cmd_install_pkg_manager(self) -> None:
        """Test ScoopPackageManager install command."""
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        cmd = pkg_manager._get_cmd_install_pkg_manager()  # pyright: ignore[reportPrivateUsage]
        assert len(cmd) > 0

    def test_get_cmd_install_dep(self) -> None:
        """Test ScoopPackageManager install dependency command."""
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        cmd = pkg_manager._get_cmd_install_dep("wget")  # pyright: ignore[reportPrivateUsage]
        assert len(cmd) > 0
