# tests\cli\pdf\test_pdf_split_cmd.py

import pytest

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, SPLIT_NAME
from file_conversor.cli.pdf.split_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfSplit:
    def test_pdf_split_cases(self, tmp_path):
        in_path = DATA_PATH / "test.pdf"
        out_path = tmp_path / "test.pdf"

        result = Test.invoke(
            COMMAND_NAME, SPLIT_NAME,
            str(in_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.with_name(f"test_1{out_path.suffix}").exists()

    def test_pdf_split_help(self,):
        Test.invoke_test_help(COMMAND_NAME, SPLIT_NAME)
