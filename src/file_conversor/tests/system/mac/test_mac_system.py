# tests/system/lin/test_mac_system.py

import pytest

from file_conversor.system import AbstractSystem, MacSystem


@pytest.mark.skipif(AbstractSystem.Platform.get() != AbstractSystem.Platform.MACOS, reason="Mac-specific tests")
class TestMacSystem:
    def test_is_admin(self,):
        assert isinstance(MacSystem.is_admin(), bool)

    def test_reload_user_path(self,):
        MacSystem.reload_user_path()
