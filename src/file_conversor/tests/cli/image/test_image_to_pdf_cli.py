# tests\cli\image\test_image_to_pdf_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageToPdfCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageToPdfCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageToPdfCLI:
    def test_image_to_pdf_cases(self, tmp_path: Path):
        in_path: Path = DATA_PATH / "test.png"
        out_path: Path = tmp_path / "test.pdf"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.TO_PDF.value,
            str(in_path),
            *TestTyper.get_out_file_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_to_pdf_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.TO_PDF.value)
