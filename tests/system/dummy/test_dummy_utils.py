# tests/system/dummy/test_dummy_utils.py

import os
import platform
import pytest

from file_conversor.system.dummy.utils import *


class TestDummyUtils:
    def test_is_admin(self,):
        assert is_admin() == False

    def test_reload_user_path(self,):
        reload_user_path()

    def test_set_window_icon(self,):
        set_window_icon("NonExistentWindowTitle", "C:\\Path\\To\\Icon.ico")
