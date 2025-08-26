# tests\cli\text\test_text__init.py

from file_conversor.cli.text._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_text_help():
    Test.invoke_test_help(COMMAND_NAME)
