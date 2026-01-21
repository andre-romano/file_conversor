
# tests\cli\pdf\test_pdf_compress_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, PdfTyperGroup
from file_conversor.cli.pdf import PdfCompressTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfCompressTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfCompress:
    def test_pdf_compress_cases(self, tmp_path):
        in_path: Path = DATA_PATH / "test.pdf"
        out_path: Path = tmp_path / "test_compressed.pdf"

        result = TestTyper.invoke(
            AppCommands.PDF.value, PdfTyperGroup.Commands.COMPRESS.value,
            str(in_path),
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_compress_help(self,):
        TestTyper.invoke_test_help(AppCommands.PDF.value, PdfTyperGroup.Commands.COMPRESS.value)
