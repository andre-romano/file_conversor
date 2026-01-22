# tests\cli\pdf\test_pdf_decrypt_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, PdfTyperGroup
from file_conversor.cli.pdf import PdfDecryptTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PdfDecryptTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfDecrypt:
    def test_pdf_decrypt_cases(self, tmp_path):
        in_path: Path = DATA_PATH / "test.pdf"
        out_path: Path = tmp_path / "test_encrypted.pdf"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.ENCRYPT.value,
            str(in_path),
            "-op", "1234",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

        in_path: Path = out_path
        out_path: Path = tmp_path / "test_encrypted_decrypted.pdf"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.DECRYPT.value,
            str(in_path),
            "-p", "1234",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_decrypt_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PDF.value, PdfTyperGroup.Commands.DECRYPT.value)
