# tests/system/lin/test_lin_utils.py

import platform
import pytest

from file_conversor.system.lin.utils import *


@pytest.mark.skipif(platform.system() != "Linux", reason="Linux-specific tests")
class TestLinUtils:
    def test_is_admin(self,):
        assert isinstance(is_admin(), bool)

    def test_reload_user_path(self,):
        reload_user_path()

    def test_set_window_icon(self,):
        set_window_icon("NonExistentWindowTitle", "C:\\Path\\To\\Icon.ico")
