# tests\cli\image\test_image_to_pdf_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, TO_PDF_NAME
from file_conversor.cli.image.to_pdf_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageToPdf:
    def test_image_to_pdf_cases(self, tmp_path):
        in_path = DATA_PATH / "test.png"
        out_path = tmp_path / "test.pdf"

        result = Test.invoke(
            COMMAND_NAME, TO_PDF_NAME,
            str(in_path),
            *Test.get_out_file_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_to_pdf_help(self,):
        Test.invoke_test_help(COMMAND_NAME, TO_PDF_NAME)
