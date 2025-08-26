# tests\cli\win\test_win_uninstall_menu_cmd.py

from file_conversor.cli.win._typer import COMMAND_NAME, UNINSTALL_MENU_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_win_uninstall_menu_help():
    Test.invoke_test_help(COMMAND_NAME, UNINSTALL_MENU_NAME)
