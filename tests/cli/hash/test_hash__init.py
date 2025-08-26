# tests\cli\hash\test__init.py

from file_conversor.cli.hash._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_hash_help():
    Test.invoke_test_help(COMMAND_NAME)
