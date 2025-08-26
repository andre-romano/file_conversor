# tests\cli\config\test__init.py

from file_conversor.cli.config._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_config_help():
    Test.invoke_test_help(COMMAND_NAME)
