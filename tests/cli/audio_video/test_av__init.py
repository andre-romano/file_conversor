
# tests/cli/audio_video/test_av__init.py

from file_conversor.cli.audio_video._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


class TestAudioVideoHelp:
    def test_audio_video_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
