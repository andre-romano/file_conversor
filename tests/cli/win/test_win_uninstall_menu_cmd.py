
from tests.utils import Test, DATA_PATH, app_cmd


def test_win_uninstall_menu_help():
    Test.invoke_test_help("win", "uninstall-menu")
