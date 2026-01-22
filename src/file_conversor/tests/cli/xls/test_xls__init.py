# tests\cli\xls\test_xls__init.py

# user-provided modules
from file_conversor.cli import AppTyperGroup, XlsTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestXlsHelp:
    def test_xls_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.XLS.value, "--help")
        for mode in XlsTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
