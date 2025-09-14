
# tests/cli/video/test_av__init.py

from file_conversor.cli.video._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


class TestVideoHelp:
    def test_video_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
