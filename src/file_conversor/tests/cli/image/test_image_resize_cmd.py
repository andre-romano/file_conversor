# tests\cli\image\test_image_resize_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, ImageTyperGroup
from file_conversor.cli.image import ImageResizeTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageResizeTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageResize:
    def test_image_resize_scale(self, tmp_path):
        in_path: Path = DATA_PATH / "test.png"
        out_path: Path = tmp_path / "test_resized.png"

        result = TestTyper.invoke(
            AppCommands.IMAGE.value, ImageTyperGroup.Commands.RESIZE.value,
            str(in_path),
            "-s", "2.0",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_resize_width(self, tmp_path):
        in_path: Path = DATA_PATH / "test.png"
        out_path: Path = tmp_path / "test_resized.png"

        result = TestTyper.invoke(
            AppCommands.IMAGE.value, ImageTyperGroup.Commands.RESIZE.value,
            str(in_path),
            "-w", "1024",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image(self,):
        TestTyper.invoke_test_help(AppCommands.IMAGE.value, ImageTyperGroup.Commands.RESIZE.value)
