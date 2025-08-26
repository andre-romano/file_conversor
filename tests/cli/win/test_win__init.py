# tests\cli\win\test_win__init.py

from file_conversor.cli.win._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_win_help():
    Test.invoke_test_help(COMMAND_NAME)
