# tests\cli\image\test_image_mirror_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageMirrorTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageMirrorTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageMirror:
    def test_image_mirror_x(self, tmp_path):
        in_path: Path = DATA_PATH / "test.png"
        out_path: Path = tmp_path / "test_mirrored.png"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.MIRROR.value,
            str(in_path),
            "-a", "x",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_mirror_y(self, tmp_path):
        in_path: Path = DATA_PATH / "test.png"
        out_path: Path = tmp_path / "test_mirrored.png"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.MIRROR.value,
            str(in_path),
            "-a", "y",
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_mirror_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.MIRROR.value)
