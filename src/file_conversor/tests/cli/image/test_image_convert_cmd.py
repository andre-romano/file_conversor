# tests\cli\image\test_image_convert_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, ImageTyperGroup
from file_conversor.cli.image import ImageConvertTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageConvertTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageConvert:
    def test_image_convert_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.png", tmp_path / "test.jpg"),
            (tmp_path / "test.jpg", tmp_path / "test.png"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppCommands.IMAGE.value, ImageTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_convert_help(self,):
        TestTyper.invoke_test_help(AppCommands.IMAGE.value, ImageTyperGroup.Commands.CONVERT.value)
