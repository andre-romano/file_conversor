# tests\cli\pdf\test_pdf_convert_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, PdfTyperGroup
from file_conversor.cli.pdf import PdfConvertTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfConvertTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfConvert:
    def test_pdf_convert_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.pdf", tmp_path / "test.jpg"),
            (DATA_PATH / "test.pdf", tmp_path / "test.png"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.with_name(f"test_1{out_path.suffix}").exists()

    def test_pdf_convert_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.CONVERT.value)
