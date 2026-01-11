# tests\cli\pdf\test_pdf_encrypt_cmd.py

import pytest

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, ENCRYPT_NAME
from file_conversor.cli.pdf.encrypt_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfEncrypt:
    def test_pdf_encrypt_cases(self, tmp_path):
        in_path = DATA_PATH / "test.pdf"
        out_path = tmp_path / "test_encrypted.pdf"

        result = Test.invoke(
            COMMAND_NAME, ENCRYPT_NAME,
            str(in_path),
            "-op", "1234",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_encrypt_help(self,):
        Test.invoke_test_help(COMMAND_NAME, ENCRYPT_NAME)
