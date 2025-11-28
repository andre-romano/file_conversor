# tests/system/test_win_utils.py

import os
import platform
import subprocess
import pytest

from file_conversor.system.win.utils import _get_window_hwnd
from file_conversor.system.win.utils import *


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific tests")
class TestWinUtils:
    def test_is_admin(self,):
        print("Is admin:", is_admin())
        assert isinstance(is_admin(), bool)

    def test_reload_user_path(self,):
        reload_user_path()
        reloaded_path = os.environ.get("PATH", "")
        assert reloaded_path != ""

    def test_restart_explorer(self,):
        # This test will restart explorer, which may disrupt the user.
        # Therefore, we will just check that the function runs without error.
        try:
            # mock subprocess.run and subprocess.Popen to prevent actual restart during test
            original_run = subprocess.run
            original_popen = subprocess.Popen
            subprocess.run = lambda *args, **kwargs: None
            subprocess.Popen = lambda *args, **kwargs: None
            restart_explorer()
        except Exception as e:
            pytest.fail(f"restart_explorer raised an exception: {e}")
        finally:
            subprocess.run = original_run
            subprocess.Popen = original_popen

    def test_get_window_hwnd(self,):
        # mock ctypes.windll.user32.FindWindowW to return a fake hwnd
        import ctypes
        original_findwindoww = ctypes.windll.user32.FindWindowW
        ctypes.windll.user32.FindWindowW = lambda *args, **kwargs: 12345  # pyright: ignore[reportAttributeAccessIssue]
        try:
            hwnd = _get_window_hwnd("NonExistentWindowTitle")
            assert hwnd == 12345
        except RuntimeError as e:
            pytest.fail(f"_get_window_hwnd raised an exception: {e}")
        finally:
            ctypes.windll.user32.FindWindowW = original_findwindoww  # pyright: ignore[reportAttributeAccessIssue]

    def test_set_window_icon(self,):
        # mock ctypes.windll.user32.FindWindowW, ctypes.windll.user32.LoadImageW, ctypes.windll.user32.SendMessageW to prevent actual window manipulation
        import ctypes
        original_findwindoww = ctypes.windll.user32.FindWindowW
        original_loadimagew = ctypes.windll.user32.LoadImageW
        original_sendmessagew = ctypes.windll.user32.SendMessageW
        ctypes.windll.user32.FindWindowW = lambda *args, **kwargs: 12345  # pyright: ignore[reportAttributeAccessIssue]
        ctypes.windll.user32.LoadImageW = lambda *args, **kwargs: 67890  # pyright: ignore[reportAttributeAccessIssue]
        ctypes.windll.user32.SendMessageW = lambda *args, **kwargs: 0  # pyright: ignore[reportAttributeAccessIssue]
        try:
            set_window_icon("NonExistentWindowTitle", "C:\\Path\\To\\Icon.ico")
        except Exception as e:
            pytest.fail(f"set_window_icon raised an exception: {e}")
        finally:
            ctypes.windll.user32.FindWindowW = original_findwindoww  # pyright: ignore[reportAttributeAccessIssue]
            ctypes.windll.user32.LoadImageW = original_loadimagew  # pyright: ignore[reportAttributeAccessIssue]
            ctypes.windll.user32.SendMessageW = original_sendmessagew  # pyright: ignore[reportAttributeAccessIssue]

    def test_set_window_icon_invalid(self,):
        import ctypes
        original_findwindoww = ctypes.windll.user32.FindWindowW
        original_loadimagew = ctypes.windll.user32.LoadImageW
        original_sendmessagew = ctypes.windll.user32.SendMessageW
        ctypes.windll.user32.FindWindowW = lambda *args, **kwargs: 12345  # pyright: ignore[reportAttributeAccessIssue]
        ctypes.windll.user32.LoadImageW = lambda *args, **kwargs: 0  # pyright: ignore[reportAttributeAccessIssue]
        ctypes.windll.user32.SendMessageW = lambda *args, **kwargs: 0  # pyright: ignore[reportAttributeAccessIssue]
        try:
            with pytest.raises(RuntimeError):
                set_window_icon("NonExistentWindowTitle", "C:\\Path\\To\\Icon.ico")
        except Exception as e:
            pytest.fail(f"set_window_icon raised an exception: {e}")
        finally:
            ctypes.windll.user32.FindWindowW = original_findwindoww  # pyright: ignore[reportAttributeAccessIssue]
            ctypes.windll.user32.LoadImageW = original_loadimagew  # pyright: ignore[reportAttributeAccessIssue]
            ctypes.windll.user32.SendMessageW = original_sendmessagew  # pyright: ignore[reportAttributeAccessIssue]
