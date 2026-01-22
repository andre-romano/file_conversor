# tests\cli\test_pdf_cmd.py

from pathlib import Path

# user-provided modules
from file_conversor.cli import AppTyperGroup, PdfTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestPdfHelp:
    def test_pdf_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.PDF.value, "--help")
        for mode in PdfTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
