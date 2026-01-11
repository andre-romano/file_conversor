
# tests\backend\test_scoop_pkg_manager.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.dependency import ScoopPackageManager

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


class TestScoopPackageManager:
    def test_get_pkg_manager_installed(self) -> None:
        """Test ScoopPackageManager when Scoop is installed."""
        if platform.system() != "Windows":
            pytest.skip("Scoop is only supported on Windows.")
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        if pkg_manager._get_pkg_manager_installed():
            assert Path(pkg_manager._get_pkg_manager_installed() or '').with_suffix("").name == "scoop"

    def test_get_supported_oses(self) -> None:
        """Test ScoopPackageManager supported OSes."""
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        supported_oses = pkg_manager._get_supported_oses()
        assert "Windows" in supported_oses

    def test_get_cmd_install_pkg_manager(self) -> None:
        """Test ScoopPackageManager install command."""
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        cmd = pkg_manager._get_cmd_install_pkg_manager()
        assert len(cmd) > 0

    def test_get_cmd_install_dep(self) -> None:
        """Test ScoopPackageManager install dependency command."""
        pkg_manager = ScoopPackageManager(dependencies={"wget": "1.21.1"})
        cmd = pkg_manager._get_cmd_install_dep("wget")
        assert len(cmd) > 0
