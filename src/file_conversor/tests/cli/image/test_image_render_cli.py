# tests\cli\image\test_image_render_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageRenderCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageRenderCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageRenderCLI:
    def test_image_render_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.svg", tmp_path / "test.jpg"),
            (DATA_PATH / "test.svg", tmp_path / "test.png"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.RENDER.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_render_help(self):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.RENDER.value)
