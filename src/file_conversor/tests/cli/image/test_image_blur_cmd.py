# tests\cli\image\test_image_blur_cmd.py

import pytest
from pathlib import Path


from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageBlurTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageBlurTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageBlur:
    def test_image_blur_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.png", tmp_path / "test_blurred.png"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.BLUR.value,
                str(in_path),
                "-r", "3",
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_blur_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.BLUR.value)
