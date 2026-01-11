# tests\cli\hash\test__init.py

from file_conversor.cli.hash._typer import COMMAND_NAME

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


class TestHashHelp:
    def test_hash_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
