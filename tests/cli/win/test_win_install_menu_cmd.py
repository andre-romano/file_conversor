
from tests.utils import Test, DATA_PATH, app_cmd


def test_win_install_menu_help():
    Test.invoke_test_help("win", "install-menu")
