# tests\cli\config\test_show_cmd.py

from file_conversor.cli.config._typer import COMMAND_NAME, SHOW_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_config_show_help():
    Test.invoke_test_help(COMMAND_NAME, SHOW_NAME)
