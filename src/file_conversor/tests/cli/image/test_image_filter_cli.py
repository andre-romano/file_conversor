# tests\cli\image\test_image_filter_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageFilterCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageFilterCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageFilterCLI:
    def test_image_filter_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.png", tmp_path / "test_filtered.png"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.FILTER.value,
                str(in_path),
                "--filter", "blur",
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_filter_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.FILTER.value)
