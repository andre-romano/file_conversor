# tests\cli\pdf\test_pdf_convert_cmd.py

import pytest

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, CONVERT_NAME
from file_conversor.cli.pdf.convert_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfConvert:
    def test_pdf_convert_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.pdf", tmp_path / "test.jpg"),
            (DATA_PATH / "test.pdf", tmp_path / "test.png"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, CONVERT_NAME,
                str(in_path),
                *Test.get_format_params(out_path),
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.with_name(f"test_1{out_path.suffix}").exists()

    def test_pdf_convert_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
