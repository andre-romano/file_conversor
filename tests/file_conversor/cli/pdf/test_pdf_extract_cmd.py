# tests\cli\pdf\test_pdf_extract_cmd.py

import pytest

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, EXTRACT_NAME
from file_conversor.cli.pdf.extract_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfExtract:
    def test_pdf_extract_cases(self, tmp_path):
        in_path = DATA_PATH / "test.pdf"
        out_path = tmp_path / "test_extracted.pdf"

        result = Test.invoke(
            COMMAND_NAME, EXTRACT_NAME,
            str(in_path),
            "-pg", "1-1",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf(self,):
        Test.invoke_test_help(COMMAND_NAME, EXTRACT_NAME)
