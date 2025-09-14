
# tests/cli/audio/test_audio__init.py

from file_conversor.cli.audio._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


class TestAudioHelp:
    def test_audio_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
