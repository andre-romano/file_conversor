# tests/system/lin/test_lin_system.py

import pytest

from file_conversor.system.lin.linux_system import AbstractSystem, LinuxSystem


@pytest.mark.skipif(AbstractSystem.Platform.get() != AbstractSystem.Platform.LINUX, reason="Linux-specific tests")
class TestLinSystem:
    def test_is_admin(self,):
        assert isinstance(LinuxSystem.is_admin(), bool)

    def test_reload_user_path(self,):
        LinuxSystem.reload_user_path()
