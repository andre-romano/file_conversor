
# tests/cli/video/test_check.py

import pytest

from file_conversor.cli.video._typer import COMMAND_NAME, CHECK_NAME
from file_conversor.cli.video.check_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoCheck:
    def test_video_check(self):
        test_cases = [
            DATA_PATH / "test.mp4",
        ]

        for in_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, CHECK_NAME,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_video_check_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CHECK_NAME)
