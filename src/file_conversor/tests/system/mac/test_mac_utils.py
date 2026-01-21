# tests/system/mac/test_mac_utils.py

import platform
import pytest

from file_conversor.system.mac.utils import *


@pytest.mark.skipif(platform.system() != "Darwin", reason="Mac-specific tests")
class TestMacUtils:
    def test_is_admin(self,):
        assert isinstance(is_admin(), bool)

    def test_reload_user_path(self,):
        reload_user_path()

    def test_set_window_icon(self,):
        set_window_icon("NonExistentWindowTitle", "C:\\Path\\To\\Icon.ico")
