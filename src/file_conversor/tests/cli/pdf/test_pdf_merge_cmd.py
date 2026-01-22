# tests\cli\pdf\test_pdf_merge_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, PdfTyperGroup
from file_conversor.cli.pdf import PdfMergeTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfMergeTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfMerge:
    def test_pdf_merge_cases(self, tmp_path):
        in_path: Path = DATA_PATH / "test.pdf"
        out_path: Path = tmp_path / "test_merged.pdf"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.MERGE.value,
            str(in_path),
            *TestTyper.get_out_file_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_merge_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.MERGE.value)
