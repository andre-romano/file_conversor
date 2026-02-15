
# tests\cli\pdf\test_pdf_compress_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, PdfTyperGroup
from file_conversor.cli.pdf import PdfCompressCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfCompressCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfCompressCLI:
    def test_pdf_compress_cases(self, tmp_path: Path):
        in_path: Path = DATA_PATH / "test.pdf"
        out_path: Path = tmp_path / "test_compressed.pdf"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.COMPRESS.value,
            str(in_path),
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_compress_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.COMPRESS.value)
