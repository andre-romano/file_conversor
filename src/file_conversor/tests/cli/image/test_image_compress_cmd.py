# tests\cli\image\test_image_compress_cmd.py

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageCompressTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageCompressTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageCompress:
    def test_image_compress_cases(self, tmp_path):
        in_path = DATA_PATH / "test.png"
        out_path = tmp_path / "test_compressed.png"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.COMPRESS.value,
            str(in_path),
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_compress_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.COMPRESS.value)
