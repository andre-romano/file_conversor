# tests\cli\image\test_image_antialias_cmd.py

from pathlib import Path

import pytest

from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageAntialiasCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageAntialiasCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageAntialiasCLI:
    def test_image_antialias_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.png", tmp_path / "test_antialiased.png"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.ANTIALIAS.value,
                str(in_path),
                "-r", "3",
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_antialias_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.ANTIALIAS.value)
