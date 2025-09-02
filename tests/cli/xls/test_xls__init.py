# tests\cli\xls\test_xls__init.py

from file_conversor.cli.xls._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH


class TestXlsHelp:
    def test_xls_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
