
# tests/cli/video/test_compress.py

import pytest

from file_conversor.cli.video._typer import COMMAND_NAME, COMPRESS_NAME
from file_conversor.cli.video.convert_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoCompress:
    def test_video_compress(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test_compressed.mkv"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, COMPRESS_NAME,
                str(in_path),
                "-ts", " 200K",
                *Test.get_format_params(out_path),
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_video_compress_help(self,):
        Test.invoke_test_help(COMMAND_NAME, COMPRESS_NAME)
