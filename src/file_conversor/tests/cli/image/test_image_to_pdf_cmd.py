# tests\cli\image\test_image_to_pdf_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, ImageTyperGroup
from file_conversor.cli.image import ImageToPdfTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageToPdfTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageToPdf:
    def test_image_to_pdf_cases(self, tmp_path):
        in_path: Path = DATA_PATH / "test.png"
        out_path: Path = tmp_path / "test.pdf"

        result = TestTyper.invoke(
            AppCommands.IMAGE.value, ImageTyperGroup.Commands.TO_PDF.value,
            str(in_path),
            *TestTyper.get_out_file_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_to_pdf_help(self,):
        TestTyper.invoke_test_help(AppCommands.IMAGE.value, ImageTyperGroup.Commands.TO_PDF.value)
