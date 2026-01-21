# tests\cli\pdf\test_pdf_extract_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, PdfTyperGroup
from file_conversor.cli.pdf import PdfExtractTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfExtractTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfExtract:
    def test_pdf_extract_cases(self, tmp_path):
        in_path: Path = DATA_PATH / "test.pdf"
        out_path: Path = tmp_path / "test_extracted.pdf"

        result = TestTyper.invoke(
            AppCommands.PDF.value, PdfTyperGroup.Commands.EXTRACT.value,
            str(in_path),
            "-pg", "1-1",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf(self,):
        TestTyper.invoke_test_help(AppCommands.PDF.value, PdfTyperGroup.Commands.EXTRACT.value)
