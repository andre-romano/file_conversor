
# tests/cli/video/test_list_formats.py

import pytest

from file_conversor.cli.video._typer import COMMAND_NAME, LIST_FORMATS_NAME
from file_conversor.cli.video.info_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoListFormats:
    def test_video_list_formats(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, LIST_FORMATS_NAME,
            )
            assert result.exit_code == 0
            assert "mp4" in result.stdout

    def test_video_list_formats_help(self,):
        Test.invoke_test_help(COMMAND_NAME, LIST_FORMATS_NAME)
