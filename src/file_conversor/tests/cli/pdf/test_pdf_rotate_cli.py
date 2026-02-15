
# tests\cli\pdf\test_pdf_rotate_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, PdfTyperGroup
from file_conversor.cli.pdf import PdfRotateCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfRotateCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfRotateCLI:
    def test_pdf_rotate_cases(self, tmp_path: Path):
        in_path: Path = DATA_PATH / "test.pdf"
        out_path: Path = tmp_path / "test_rotated.pdf"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.ROTATE.value,
            str(in_path),
            "-r", "1-:90",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_rotate_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.ROTATE.value)
