# tests\cli\pdf\test_pdf_extract_img_cmd.py

import pytest

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, EXTRACT_IMG_NAME
from file_conversor.cli.pdf.extract_img_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfExtractImg:
    def test_pdf_extract_img_cases(self, tmp_path):
        in_path = DATA_PATH / "test.pdf"
        out_path = tmp_path / "test.pdf"

        result = Test.invoke(
            COMMAND_NAME, EXTRACT_IMG_NAME,
            str(in_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0

    def test_pdf_extract_img_help(self,):
        Test.invoke_test_help(COMMAND_NAME, EXTRACT_IMG_NAME)
