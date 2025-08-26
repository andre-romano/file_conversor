# tests\cli\win\test_win_install_menu_cmd.py

from file_conversor.cli.win._typer import COMMAND_NAME, INSTALL_MENU_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_win_install_menu_help():
    Test.invoke_test_help(COMMAND_NAME, INSTALL_MENU_NAME)
