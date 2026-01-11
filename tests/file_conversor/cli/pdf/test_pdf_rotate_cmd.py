
# tests\cli\pdf\test_pdf_rotate_cmd.py

import pytest

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, ROTATE_NAME
from file_conversor.cli.pdf.rotate_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPdfRotate:
    def test_pdf_rotate_cases(self, tmp_path):
        in_path = DATA_PATH / "test.pdf"
        out_path = tmp_path / "test_rotated.pdf"

        result = Test.invoke(
            COMMAND_NAME, ROTATE_NAME,
            str(in_path),
            "-r", "1-:90",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_pdf_rotate_help(self,):
        Test.invoke_test_help(COMMAND_NAME, ROTATE_NAME)
